from flask import Flask, render_template, request, jsonify
from email_service import EmailService
from news_service import NewsService
from groq_service import GroqService
import os



app = Flask(__name__)
app.secret_key = 'your-secret-key'

EMAIL_USER = 'kaviya.sha24@gmail.com'
EMAIL_PASS = "njlh trdm sbhq lggr"

groq_service = GroqService(api_key="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")
email_service = EmailService(groq_service, EMAIL_USER, EMAIL_PASS)
news_service = NewsService(groq_service)

@app.route('/')
def index():
    return render_template('index.html')

# Email summary page (email.html)
@app.route('/email_summary')
def email_summary():
    print("fetching thee email...")
    emails = email_service.fetch_emails()
    print(emails)
    for i in range(min(2, len(emails))):
        if emails[i]['body']:
            
            emails[i]['summary'] = groq_service.get_summary(emails[i]['body'], is_email=True)

    return render_template('email.html', emails=emails)

# Handle dynamic summarization of emails via POST (AJAX)
@app.route('/summarize_email', methods=['POST'])
def summarize_email():
    index = int(request.form.get('email_id', -1))
    emails = email_service.fetch_emails()

    if 0 <= index < len(emails):
        summary = groq_service.get_summary(emails[index]['body'], is_email=True)
        return jsonify({'summary': summary})

    return jsonify({'error': 'Invalid email index'}), 400


@app.route('/news_summary')
def news_summary():
    news_sources = [
        {'name': 'BBC', 'url': 'https://www.bbc.com/news'},
        {'name': 'business', 'url': 'https://www.bbc.com/news/articles/c62znepddq4o'},
        {'name': 'sport', 'url': 'https://www.bbc.com/sport/cricket/articles/cr4nq35ezgro'}
    ]
    return render_template('news.html', news_sources=news_sources)

@app.route('/summarize_news', methods=['POST'])
def summarize_news():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        article_content = news_service.scrape_article(url)
        if article_content:
            summary = groq_service.get_summary(article_content, is_email=False)
            return jsonify({'summary': summary})
        else:
            return jsonify({'error': 'Could not extract article content'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
