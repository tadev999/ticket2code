#!/usr/bin/env python3
"""
Design Image Analysis using Python + OpenCV
Analyzes design screenshots to extract:
- Component boundaries (contour detection)
- Colors (dominant palette, color sampling)
- Layout structure (positions, sizes, spacing estimates)
- Text regions (optional OCR with pytesseract)

Usage:
  python3 image_analyze.py --input-folder docs/figma_design_analysis/TICKET_screenshots
  python3 image_analyze.py --input-folder docs/figma_design_analysis/TICKET_screenshots --extract-text
"""

import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple

try:
    import cv2
    import numpy as np
    from PIL import Image
except ImportError as e:
    print(f"Error: Required libraries not found: {e}")
    print("Install with: pip install opencv-python numpy pillow")
    sys.exit(1)

# Optional: try importing pytesseract for text extraction
try:
    import pytesseract
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False


class ImageAnalyzer:
    """Analyze design screenshots using OpenCV + image processing."""
    
    def __init__(self, input_folder: str, ticket_id: str, extract_text: bool = False, debug: bool = False):
        self.input_folder = Path(input_folder)
        self.ticket_id = ticket_id
        self.extract_text = extract_text and HAS_PYTESSERACT
        self.debug = debug
        self.images = []
        self.analysis_results = []
        self.min_area = 400  # minimum component box area in pixels
        
    def load_images(self) -> List[str]:
        """Load supported image files from folder."""
        supported_formats = ('.png', '.jpg', '.jpeg', '.webp')
        images = sorted([
            f for f in os.listdir(self.input_folder)
            if f.lower().endswith(supported_formats)
        ])
        
        if not images:
            print(f"No supported images found in {self.input_folder}")
            return []
        
        self.images = images
        print(f"Found {len(images)} images: {', '.join(images[:3])}{'...' if len(images) > 3 else ''}")
        return images
    
    def extract_colors(self, image: np.ndarray, num_colors: int = 5, sample_max_dim: int = 200) -> List[Dict[str, Any]]:
        """Extract dominant colors via k-means on a downsampled copy (fast + stable)."""
        if image is None or image.size == 0:
            return []
        h, w = image.shape[:2]
        longest = max(h, w)
        scale = min(1.0, sample_max_dim / float(longest)) if longest > 0 else 1.0
        if scale < 1.0:
            small = cv2.resize(
                image,
                (max(1, int(w * scale)), max(1, int(h * scale))),
                interpolation=cv2.INTER_AREA,
            )
        else:
            small = image

        pixels = small.reshape((-1, 3)).astype(np.float32)
        if pixels.shape[0] == 0:
            return []

        k = int(min(num_colors, pixels.shape[0]))
        if k < 1:
            return []

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 5, cv2.KMEANS_PP_CENTERS)
        labels = labels.flatten()
        counts = np.bincount(labels, minlength=k)
        total = int(counts.sum()) or 1
        centers_u8 = np.uint8(centers)

        unique_colors = []
        for idx in range(k):
            b, g, r = centers_u8[idx].tolist()  # OpenCV is BGR
            rgb = (int(r), int(g), int(b))
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
            unique_colors.append({
                'hex': hex_color,
                'rgb': rgb,
                'frequency': int(counts[idx]),
                'ratio': round(float(counts[idx]) / total, 4),
            })

        unique_colors.sort(key=lambda x: x['frequency'], reverse=True)
        return unique_colors[:num_colors]

    @staticmethod
    def _overlap_ratio(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> float:
        """Intersection area over the smaller box area (0..1)."""
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        ix1, iy1 = max(ax, bx), max(ay, by)
        ix2, iy2 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
        iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
        inter = iw * ih
        if inter == 0:
            return 0.0
        smaller = min(aw * ah, bw * bh) or 1
        return inter / float(smaller)
    
    def detect_components(self, image: np.ndarray, image_path: str) -> List[Dict[str, Any]]:
        """Detect component boundaries using Canny edges + morphology + box merging."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # Content-adaptive Canny thresholds (robust to light/dark themes)
        med = float(np.median(gray))
        lower = int(max(0, 0.66 * med))
        upper = int(min(255, 1.33 * med))
        edges = cv2.Canny(gray, lower, upper)

        # Close gaps so edges of a UI element form a single region
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        closed = cv2.dilate(edges, kernel, iterations=2)

        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img_h, img_w = gray.shape[:2]
        img_area = img_h * img_w
        min_area = max(self.min_area, int(0.0005 * img_area))

        raw_boxes: List[Tuple[int, int, int, int]] = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            if area < min_area:
                continue
            if area > 0.98 * img_area:  # skip full-frame background
                continue
            raw_boxes.append((int(x), int(y), int(w), int(h)))

        # Merge: keep larger boxes, drop those mostly contained in a kept box
        raw_boxes.sort(key=lambda b: b[2] * b[3], reverse=True)
        kept: List[Tuple[int, int, int, int]] = []
        for box in raw_boxes:
            if any(self._overlap_ratio(box, k) > 0.85 for k in kept):
                continue
            kept.append(box)

        components = []
        for (x, y, w, h) in kept:
            region = image[y:y + h, x:x + w]
            colors = self.extract_colors(region, num_colors=1)
            components.append({
                'position': {'x': int(x), 'y': int(y)},
                'size': {'width': int(w), 'height': int(h)},
                'area': int(w * h),
                'background_color': colors[0] if colors else None,
                'confidence': 'medium',  # heuristic estimate
            })

        components.sort(key=lambda c: (c['position']['y'], c['position']['x']))

        if self.debug:
            debug_img = image.copy()
            for comp in components:
                x = comp['position']['x']
                y = comp['position']['y']
                w = comp['size']['width']
                h = comp['size']['height']
                cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            debug_path = Path(self.input_folder) / f"debug_{Path(image_path).name}"
            cv2.imwrite(str(debug_path), debug_img)
            print(f"  Debug visualization saved: {debug_path}")

        return components
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze single image."""
        full_path = self.input_folder / image_path

        print(f"\nAnalyzing: {image_path}")

        # Read image
        image = cv2.imread(str(full_path))
        if image is None:
            print(f"  Error: Could not load image")
            return {'error': 'Failed to load image', 'file': image_path}

        height, width = image.shape[:2]
        print(f"  Dimensions: {width}x{height}")

        # Infer render scale (@1x/@2x/@3x) and device so specs can be given in points
        scale_info = self.infer_scale_device(width, height)
        scale = scale_info['scale']
        print(f"  Device: {scale_info['device']} (@{scale}x, {scale_info['confidence']} confidence)")

        # Extract colors
        colors = self.extract_colors(image)
        print(f"  Dominant colors: {[c['hex'] for c in colors[:3]]}")

        # Detect components
        components = self.detect_components(image, image_path)
        print(f"  Components detected: {len(components)}")

        # Layout relations: gaps, alignment groups, spacing grid
        layout = self.compute_layout_relations(components, scale)

        result = {
            'file': image_path,
            'dimensions': {'width': width, 'height': height},
            'scale': scale,
            'device': scale_info['device'],
            'orientation': scale_info['orientation'],
            'logical_size_pt': {
                'width': scale_info['logical'][0],
                'height': scale_info['logical'][1],
            },
            'scale_confidence': scale_info['confidence'],
            'colors': colors,
            'components': components,
            'layout': layout,
            'timestamp': datetime.now().isoformat(),
        }

        # Optional: extract text + estimate typography
        if self.extract_text:
            print("  Extracting text regions (pytesseract)...")
            text_regions = self._extract_text_regions(image)
            result['text_regions'] = text_regions
            result['typography'] = self.estimate_typography(image, text_regions, scale)

        return result
    
    def _extract_text_regions(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Extract text regions using pytesseract."""
        try:
            # Use Tesseract to get bounding boxes
            results = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            text_regions = []
            for i in range(len(results['text'])):
                text = results['text'][i].strip()
                if text:  # Only non-empty
                    text_regions.append({
                        'text': text,
                        'position': {
                            'x': int(results['left'][i]),
                            'y': int(results['top'][i])
                        },
                        'size': {
                            'width': int(results['width'][i]),
                            'height': int(results['height'][i])
                        },
                        'confidence': float(results['conf'][i])
                    })
            
            return text_regions
        except Exception as e:
            print(f"  Warning: Text extraction failed: {e}")
            return []

    # Known logical sizes (points) and native render scale for device inference.
    KNOWN_DEVICES = [
        ("iPhone SE / 8 / 7 / 6s", 375, 667, 2),
        ("iPhone 8 Plus", 414, 736, 3),
        ("iPhone X / XS / 11 Pro / 13 mini", 375, 812, 3),
        ("iPhone 12 / 13 / 14", 390, 844, 3),
        ("iPhone 14 Pro / 15 / 15 Pro", 393, 852, 3),
        ("iPhone XR / 11", 414, 896, 2),
        ("iPhone 14 Plus", 428, 926, 3),
        ("iPhone 14 Pro Max / 15 Pro Max", 430, 932, 3),
        ("iPad 10.2", 810, 1080, 2),
        ("iPad Pro 11", 834, 1194, 2),
        ("iPad Pro 12.9", 1024, 1366, 2),
        ("Android (baseline mdpi)", 360, 640, 1),
        ("Android (common xxhdpi)", 360, 800, 3),
    ]

    def infer_scale_device(self, width: int, height: int) -> Dict[str, Any]:
        """Best-effort device + render-scale inference from pixel dimensions."""
        best = None
        for name, lw, lh, scale in self.KNOWN_DEVICES:
            for pw, ph in ((lw * scale, lh * scale), (lh * scale, lw * scale)):
                dw = abs(width - pw) / max(pw, 1)
                dh = abs(height - ph) / max(ph, 1)
                score = dw + dh
                if score < 0.03 and (best is None or score < best['_score']):
                    if width <= height:
                        logical = (lw, lh)
                    else:
                        logical = (lh, lw)
                    best = {
                        'device': name,
                        'scale': scale,
                        'orientation': 'portrait' if height >= width else 'landscape',
                        'logical': logical,
                        'confidence': 'high',
                        '_score': score,
                    }
        if best:
            best.pop('_score', None)
            return best

        # Fallback: guess scale by magnitude of the long side
        long_side = max(width, height)
        if long_side >= 2000:
            scale = 3
        elif long_side >= 1000:
            scale = 2
        else:
            scale = 1
        return {
            'device': 'unknown',
            'scale': scale,
            'orientation': 'portrait' if height >= width else 'landscape',
            'logical': (round(width / scale), round(height / scale)),
            'confidence': 'low',
        }

    def compute_layout_relations(self, components: List[Dict[str, Any]], scale: float) -> Dict[str, Any]:
        """Derive alignment groups, inter-component gaps, and spacing grid (in points)."""
        rels: Dict[str, Any] = {
            'alignment_groups': {'left_aligned': [], 'right_aligned': [], 'center_x_aligned': []},
            'vertical_gaps_pt': [],
            'horizontal_gaps_pt': [],
            'spacing_scale': {'base_grid_pt': None, 'grid_fit_ratio_8': 0.0,
                              'grid_fit_ratio_4': 0.0, 'common_gaps_pt': []},
        }
        n = len(components)
        if n == 0:
            return rels

        def to_pt(v: float) -> float:
            return round(v / scale, 1) if scale else float(v)

        widths = [c['size']['width'] for c in components]
        tol = max(2, int(0.01 * max(widths)))

        def group_by(key_fn):
            groups: Dict[int, List[int]] = {}
            for i, c in enumerate(components):
                key = key_fn(c)
                placed = False
                for gk in groups:
                    if abs(gk - key) <= tol:
                        groups[gk].append(i)
                        placed = True
                        break
                if not placed:
                    groups[key] = [i]
            return [sorted(v) for v in groups.values() if len(v) >= 2]

        rels['alignment_groups']['left_aligned'] = group_by(lambda c: c['position']['x'])
        rels['alignment_groups']['right_aligned'] = group_by(
            lambda c: c['position']['x'] + c['size']['width'])
        rels['alignment_groups']['center_x_aligned'] = group_by(
            lambda c: c['position']['x'] + c['size']['width'] // 2)

        for i in range(n):
            a = components[i]
            ax, aw = a['position']['x'], a['size']['width']
            ay2 = a['position']['y'] + a['size']['height']
            ay, ah = a['position']['y'], a['size']['height']
            for j in range(n):
                if i == j:
                    continue
                b = components[j]
                bx, bw = b['position']['x'], b['size']['width']
                by, bh = b['position']['y'], b['size']['height']
                # Vertical gap: horizontally overlapping, b below a
                if min(ax + aw, bx + bw) - max(ax, bx) > 0:
                    gap = by - ay2
                    if 0 < gap < 400:
                        rels['vertical_gaps_pt'].append(to_pt(gap))
                # Horizontal gap: vertically overlapping, b right of a
                if min(ay + ah, by + bh) - max(ay, by) > 0:
                    gap = bx - (ax + aw)
                    if 0 < gap < 400:
                        rels['horizontal_gaps_pt'].append(to_pt(gap))

        rels['spacing_scale'] = self._infer_spacing_scale(
            rels['vertical_gaps_pt'] + rels['horizontal_gaps_pt'])
        return rels

    @staticmethod
    def _infer_spacing_scale(gaps: List[float]) -> Dict[str, Any]:
        """Detect whether gaps fit a 4/8pt grid and list the most common gap values."""
        from collections import Counter
        rounded = [int(round(g)) for g in gaps if g > 0]
        if not rounded:
            return {'base_grid_pt': None, 'grid_fit_ratio_8': 0.0,
                    'grid_fit_ratio_4': 0.0, 'common_gaps_pt': []}
        f8 = sum(1 for g in rounded if g % 8 == 0) / len(rounded)
        f4 = sum(1 for g in rounded if g % 4 == 0) / len(rounded)
        base = 8 if f8 >= 0.6 else (4 if f4 >= 0.6 else None)
        common = [v for v, _ in Counter(rounded).most_common(6)]
        return {
            'base_grid_pt': base,
            'grid_fit_ratio_8': round(f8, 2),
            'grid_fit_ratio_4': round(f4, 2),
            'common_gaps_pt': sorted(common),
        }

    def estimate_typography(self, image: np.ndarray, text_regions: List[Dict[str, Any]],
                            scale: float) -> List[Dict[str, Any]]:
        """Estimate font size (pt) and text color per OCR text box (low confidence)."""
        out = []
        for r in text_regions:
            x = max(0, r['position']['x'])
            y = max(0, r['position']['y'])
            w = r['size']['width']
            h = r['size']['height']
            font_pt = round(h / scale, 1) if scale else float(h)

            text_color = None
            region = image[y:y + h, x:x + w]
            if region.size:
                cols = self.extract_colors(region, num_colors=2)
                # Heuristic: the less frequent cluster tends to be the glyph color
                if len(cols) >= 2:
                    text_color = cols[-1]['hex']
                elif cols:
                    text_color = cols[0]['hex']

            out.append({
                'text': r['text'],
                'font_size_pt_est': font_pt,
                'box_height_px': int(h),
                'text_color_est': text_color,
                'position': r['position'],
                'confidence': 'low',
            })
        return out

    def analyze_all(self):
        """Analyze all images in folder."""
        self.load_images()
        
        for image_path in self.images:
            result = self.analyze_image(image_path)
            self.analysis_results.append(result)
        
        return self.analysis_results
    
    def generate_markdown_report(self, output_path: str = None) -> str:
        """Generate markdown report from analysis results."""
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d%H%M')
            output_path = f"docs/design/{self.ticket_id}_image_analysis_{timestamp}.md"

        lines = [
            f"# Design Image Analysis Report",
            f"**Ticket:** {self.ticket_id}",
            f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Method:** Python + OpenCV Image Analysis",
            f"**Accuracy:** ~70-80% (estimated from contours, colors, and spacing heuristics)",
            "",
            "## Summary",
        ]

        for result in self.analysis_results:
            if 'error' in result:
                lines.append(f"- [FAIL] {result['file']}: {result['error']}")
            else:
                lines.append(
                    f"- [OK] {result['file']}: "
                    f"{result['dimensions']['width']}x{result['dimensions']['height']}px "
                    f"@{result.get('scale', '?')}x, {len(result.get('components', []))} components"
                )

        lines.extend([
            "",
            "## Detailed Analysis",
        ])

        for result in self.analysis_results:
            if 'error' in result:
                continue

            scale = result.get('scale', 1)
            logical = result.get('logical_size_pt', {})
            lines.extend([
                f"### {result['file']}",
                "",
                "#### Screen Properties",
                "| Property | Value |",
                "|---|---|",
                f"| Device (inferred) | {result.get('device', 'unknown')} |",
                f"| Render scale | @{scale}x ({result.get('scale_confidence', 'low')} confidence) |",
                f"| Orientation | {result.get('orientation', 'unknown')} |",
                f"| Pixel size | {result['dimensions']['width']}x{result['dimensions']['height']} px |",
                f"| Logical size | {logical.get('width', '?')}x{logical.get('height', '?')} pt |",
                "",
                "#### Dominant Colors",
                "| Hex Color | RGB | Ratio |",
                "|---|---|---|",
            ])

            for c in result['colors'][:8]:
                lines.append(f"| {c['hex']} | {c['rgb']} | {c.get('ratio', 0)} |")

            lines.extend([
                "",
                "#### Detected Components (position/size in points)",
                "| # | Position (pt) | Size (pt) | Background | Confidence |",
                "|---|---|---|---|---|",
            ])

            for idx, comp in enumerate(result['components'], start=1):
                bg = comp.get('background_color') or {}
                bg_hex = bg.get('hex', 'N/A')
                px = round(comp['position']['x'] / scale, 1) if scale else comp['position']['x']
                py = round(comp['position']['y'] / scale, 1) if scale else comp['position']['y']
                pw = round(comp['size']['width'] / scale, 1) if scale else comp['size']['width']
                ph = round(comp['size']['height'] / scale, 1) if scale else comp['size']['height']
                lines.append(
                    f"| {idx} | ({px}, {py}) | {pw}x{ph} | {bg_hex} | {comp['confidence']} |"
                )

            # Layout relations
            layout = result.get('layout', {})
            spacing = layout.get('spacing_scale', {})
            groups = layout.get('alignment_groups', {})
            lines.extend([
                "",
                "#### Layout Relations",
                f"- Base spacing grid: {spacing.get('base_grid_pt') or 'not detected'} pt "
                f"(8pt fit {spacing.get('grid_fit_ratio_8', 0)}, 4pt fit {spacing.get('grid_fit_ratio_4', 0)})",
                f"- Common gaps (pt): {spacing.get('common_gaps_pt', [])}",
                f"- Left-aligned groups (component #): {groups.get('left_aligned', [])}",
                f"- Right-aligned groups (component #): {groups.get('right_aligned', [])}",
                f"- Center-x-aligned groups (component #): {groups.get('center_x_aligned', [])}",
            ])

            # Typography (from OCR estimation)
            if result.get('typography'):
                lines.extend([
                    "",
                    "#### Typography (estimated from OCR)",
                    "| Text | Font size (pt, est) | Text color (est) | Position (px) | Confidence |",
                    "|---|---|---|---|---|",
                ])
                for t in result['typography']:
                    lines.append(
                        f"| {t['text']} | {t['font_size_pt_est']} | {t.get('text_color_est', 'N/A')} | "
                        f"({t['position']['x']}, {t['position']['y']}) | {t['confidence']} |"
                    )
            elif result.get('text_regions'):
                lines.extend([
                    "",
                    "#### Extracted Text Regions",
                    "| Text | Position (px) | Size (px) | OCR confidence |",
                    "|---|---|---|---|",
                ])
                for region in result['text_regions']:
                    lines.append(
                        f"| {region['text']} | "
                        f"({region['position']['x']}, {region['position']['y']}) | "
                        f"{region['size']['width']}x{region['size']['height']} | "
                        f"{region['confidence']:.1f} |"
                    )

            lines.append("")

        # Add notes section
        lines.extend([
            "## Manual Refinements Required",
            "",
            "The above analysis is automated and estimated. Please refine using `notes.md`:",
            "",
            "```markdown",
            "## Layout Refinements",
            "",
            "### Component: [ComponentName]",
            "Semantic role: [description]",
            "Padding: [top, right, bottom, left]",
            "Margin: [top, right, bottom, left]",
            "Font refinements: [if needed]",
            "```",
            "",
            "## Integration Notes",
            "- Position/size in the tables are already converted to points using the inferred @Nx scale.",
            "- If the device/scale inference confidence is low, verify the scale before using point values.",
            "- Colors are detected from pixel sampling; verify tokens with the design tool.",
            "- Component boundaries are estimated from edge detection; merge/adjust as needed.",
            "- Spacing grid and alignment groups are heuristics to seed layout constraints, not exact specs.",
            "- For precise specs, combine with manual annotations in `notes.md`.",
        ])

        markdown = "\n".join(lines)

        # Write to file
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(markdown)

        print(f"\n[OK] Report saved to: {output_path}")
        return markdown
    
    def export_json(self, output_path: str = None) -> str:
        """Export analysis results as JSON."""
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d%H%M')
            output_path = f"docs/design/{self.ticket_id}_layout_specs_{timestamp}.json"
        
        json_data = {
            'ticket': self.ticket_id,
            'timestamp': datetime.now().isoformat(),
            'method': 'Python + OpenCV',
            'images': self.analysis_results
        }
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"[OK] JSON specs saved to: {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Analyze design screenshots using Python + OpenCV'
    )
    parser.add_argument('--input-folder', required=True, help='Input folder with screenshots')
    parser.add_argument('--ticket-id', required=True, help='JIRA ticket ID')
    parser.add_argument('--output', help='Output markdown file path')
    parser.add_argument('--extract-text', action='store_true', help='Extract text regions (requires pytesseract)')
    parser.add_argument('--debug', action='store_true', help='Save debug visualization images')
    
    args = parser.parse_args()
    
    analyzer = ImageAnalyzer(
        input_folder=args.input_folder,
        ticket_id=args.ticket_id,
        extract_text=args.extract_text,
        debug=args.debug
    )
    
    # Analyze all images
    analyzer.analyze_all()
    
    # Generate reports
    analyzer.generate_markdown_report(args.output)
    analyzer.export_json()
    
    print("\n[OK] Analysis complete!")


if __name__ == '__main__':
    main()
