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
    from skimage import color, exposure
except ImportError as e:
    print(f"Error: Required libraries not found: {e}")
    print("Install with: pip install opencv-python numpy pillow scikit-image")
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
    
    def extract_colors(self, image: np.ndarray, num_colors: int = 5) -> List[Dict[str, Any]]:
        """Extract dominant colors from image."""
        # Reshape image to 2D array of pixels
        pixels = image.reshape((-1, 3))
        pixels = np.float32(pixels)
        
        # K-means clustering to find dominant colors
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        centers = np.uint8(centers)
        unique_colors = []
        
        for color in centers:
            # Convert BGR to RGB
            rgb = tuple(reversed(color.tolist()))
            # Convert to hex
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
            unique_colors.append({
                'hex': hex_color,
                'rgb': rgb,
                'frequency': int(np.sum(labels == len(unique_colors)))
            })
        
        # Sort by frequency
        unique_colors.sort(key=lambda x: x['frequency'], reverse=True)
        return unique_colors[:num_colors]
    
    def detect_components(self, image: np.ndarray, image_path: str) -> List[Dict[str, Any]]:
        """Detect component boundaries using edge detection and contours."""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        components = []
        min_area = 100  # Filter small noise
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area:
                continue
            
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Extract region for color analysis
            region = image[y:y+h, x:x+w]
            colors = self.extract_colors(region, num_colors=1)
            
            components.append({
                'position': {'x': int(x), 'y': int(y)},
                'size': {'width': int(w), 'height': int(h)},
                'area': int(area),
                'background_color': colors[0] if colors else None,
                'confidence': 'medium'  # Heuristic estimate
            })
        
        # Sort by position (top-left to bottom-right)
        components.sort(key=lambda c: (c['position']['y'], c['position']['x']))
        
        if self.debug:
            # Save debug visualization
            debug_img = image.copy()
            for comp in components:
                x = comp['position']['x']
                y = comp['position']['y']
                w = comp['size']['width']
                h = comp['size']['height']
                cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
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
        
        # Extract colors
        colors = self.extract_colors(image)
        print(f"  Dominant colors: {[c['hex'] for c in colors[:3]]}")
        
        # Detect components
        components = self.detect_components(image, image_path)
        print(f"  Components detected: {len(components)}")
        
        result = {
            'file': image_path,
            'dimensions': {'width': width, 'height': height},
            'colors': colors,
            'components': components,
            'timestamp': datetime.now().isoformat()
        }
        
        # Optional: extract text
        if self.extract_text:
            print("  Extracting text regions (pytesseract)...")
            text_regions = self._extract_text_regions(image)
            result['text_regions'] = text_regions
        
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
            f"**Accuracy:** ~70-80% (estimated from contours and colors)",
            "",
            "## Summary",
        ]
        
        for result in self.analysis_results:
            if 'error' in result:
                lines.append(f"- ❌ {result['file']}: {result['error']}")
            else:
                lines.append(f"- ✅ {result['file']}: {result['dimensions']['width']}x{result['dimensions']['height']}, {len(result.get('components', []))} components")
        
        lines.extend([
            "",
            "## Detailed Analysis",
        ])
        
        for result in self.analysis_results:
            if 'error' in result:
                continue
            
            lines.extend([
                f"### {result['file']}",
                f"**Dimensions:** {result['dimensions']['width']}x{result['dimensions']['height']}",
                "",
                "#### Dominant Colors",
                "| Hex Color | RGB | Frequency |",
                "|---|---|---|",
            ])
            
            for color in result['colors'][:5]:
                lines.append(f"| {color['hex']} | {color['rgb']} | {color['frequency']} |")
            
            lines.extend([
                "",
                "#### Detected Components",
                "| Position | Size | Background Color | Confidence |",
                "|---|---|---|---|",
            ])
            
            for comp in result['components'][:10]:
                bg_color = comp.get('background_color', {}).get('hex', 'N/A') if comp.get('background_color') else 'N/A'
                lines.append(
                    f"| ({comp['position']['x']}, {comp['position']['y']}) | "
                    f"{comp['size']['width']}x{comp['size']['height']} | "
                    f"{bg_color} | "
                    f"{comp['confidence']} |"
                )
            
            if len(result['components']) > 10:
                lines.append(f"... and {len(result['components']) - 10} more components")
            
            # Add text regions if available
            if result.get('text_regions'):
                lines.extend([
                    "",
                    "#### Extracted Text Regions",
                    "| Text | Position | Size | Confidence |",
                    "|---|---|---|---|",
                ])
                
                for region in result['text_regions'][:10]:
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
            "- Position/size values are in pixels; convert to points (÷2 for @2x) if needed",
            "- Colors are detected from pixel sampling; verify with design tool",
            "- Component boundaries estimated from edge detection; may need manual adjustment",
            "- For precise specs, combine with manual annotations in `notes.md`",
        ])
        
        markdown = "\n".join(lines)
        
        # Write to file
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(markdown)
        
        print(f"\n✅ Report saved to: {output_path}")
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
        
        print(f"✅ JSON specs saved to: {output_path}")
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
    
    print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()
