# MyBlog

A simple personal blog application built with Django, featuring a clean interface for writing and sharing blog posts with commenting functionality and email sharing capabilities.

## Features

 **Blog Management**: Create, edit, and publish blog posts through Django admin
 **Comment System**: Readers can comment on blog posts
 **Email Sharing**: Share interesting posts via email
 **Tagging System**: Organize posts with tags using django-taggit
 **User Management**: Admin authentication for content management
 **Date-based URLs**: SEO-friendly URLs with publication dates
 **Draft/Published Status**: Control post visibility

## Tech Stack

- **Backend**: Django 5.1.6
- **Database**: PostgreSQL 16.2 (Docker containerized)
- **Frontend**: HTML templates with Django templating engine
- **Additional Libraries**:
  - django-taggit (tagging system)
  - python-decouple (environment variables)
  - psycopg (PostgreSQL adapter)

## Prerequisites

Before running this project, make sure you have:

- Python 3.8+
- Docker (for PostgreSQL container)
- Git

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd mysite
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL with Docker
```bash
# Pull and run PostgreSQL 16.2 container
docker run --name postgres-blog \
  -e POSTGRES_DB=your_db_name \
  -e POSTGRES_USER=your_db_user \
  -e POSTGRES_PASSWORD=your_db_password \
  -p 5432:5432 \
  -d postgres:16.2
```

### 5. Environment Configuration
Create a `.env` file in the project root directory:

```env
# Database Configuration
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (for sharing posts)
EMAIL_HOST_USER=your_gmail@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_gmail@gmail.com
```

**Note**: For Gmail, you'll need to use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

### 6. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at:
- **Blog**: http://127.0.0.1:8000/blog/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Usage

### Creating Blog Posts
1. Access the admin panel at `/admin/`
2. Log in with your superuser credentials
3. Navigate to **Posts** under the **BLOG** section
4. Click **Add Post** to create a new blog entry
5. Fill in the title, content, tags, and set status to "Published"
6. Save the post

### Managing Comments
- Comments are automatically displayed on blog posts
- Moderate comments through the admin panel under **Comments**
- Toggle comment visibility using the "Active" checkbox

### Sharing Posts
- Each blog post has a "Share via Email" feature
- Readers can share posts by providing recipient email addresses
- Emails are sent through the configured Gmail SMTP

## Project Structure

```
mysite/
├── my_site/              # Main project directory
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── blog/                # Blog application
│   ├── models.py        # Database models (Post, Comment)
│   ├── views.py         # View functions
│   ├── urls.py          # Blog URL patterns
│   ├── admin.py         # Admin configuration
│   └── templates/       # HTML templates
├── requirements.txt     # Python dependencies
└── manage.py           # Django management script
```

## URL Patterns

- `/blog/` - Blog post list
- `/blog/tag/<tag-name>/` - Posts filtered by tag
- `/blog/YYYY/MM/DD/post-slug/` - Individual post detail
- `/blog/<post-id>/share/` - Email sharing form
- `/blog/<post-id>/comment/` - Comment submission
- `/admin/` - Django admin interface

## Development Notes

### Database Models
- **Post**: Main blog post model with title, content, author, publish date, and status
- **Comment**: User comments linked to posts with moderation capability

### Key Features Implementation
- **Custom Manager**: `PublishedManager` filters only published posts
- **Slug Generation**: SEO-friendly URLs with date-based routing
- **Tagging**: Integrated django-taggit for flexible post categorization
- **Email Integration**: SMTP configuration for post sharing

## Security Considerations

⚠️ **Important**: This setup is for development only.

