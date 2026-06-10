# Hướng dẫn cài đặt lần đầu

Mục tiêu: cài xong và chạy được command `/ticket TICKET-XXXXX` ngay.

## 1) Thêm file vào repo

1. Copy file ticket.prompt.md vào thư mục `.github/prompts/`của repo
2. Copy `ticket2code` folder vào repo

## 2) Tạo `.env.local`

Tạo `.env.local` ở root repo với nội dung:

```dotenv
JIRA_TOKEN=your_token_here
JIRA_EMAIL=your_atlassian_email@company.com
JIRA_URL=your_jira_base_url
```

## 3) Kiểm tra cấu trúc thư mục

```text
your-repo/
|-- .env.local
|-- .github/
|   `-- prompts/
|       `-- ticket.prompt.md
`-- ticket2code/
    `-- ticket/
        |-- ticket-processor.prompt.md
        |-- ticket-agent.md
        |-- ticket.prompt.md
        |-- env.local.example
        `-- SETUP.md
```

## 4) Điều kiện để chạy ổn định

- Repo cần có rule trong `docs/` cho các nhóm: coding style, code review, logging, test, development policy, bug-pattern/release-bug.
- Có thể dùng thêm file instruction ở mức repo nếu cần ràng buộc bổ sung.

## 5) Cách chạy

Mở Copilot Chat và chạy:

```text
/ticket TICKET-XXXXX
```

## 6) Bảo mật

- Không commit `.env.local` thật.
- Không gửi `JIRA_TOKEN` qua chat/email.