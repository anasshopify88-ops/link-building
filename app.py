import streamlit as st
from playwright.sync_api import sync_playwright
import random
import time

# --- واجهة المستخدم ---
st.title("💬 Auto Comment Backlink Builder")

# بيانات المعلق
name = st.sidebar.text_input("الاسم (Anchor Text)", "Seo Expert")
email = st.sidebar.text_input("الايميل", "myemail@example.com")
website = st.sidebar.text_input("رابط موقعك (Backlink)", "https://mysite.com")

# التعليقات (يفضل وضع عدة صياغات لتجنب السبام)
comments_list = st.sidebar.text_area("التعليقات (تعليق واحد في كل سطر)", 
    "مقال رائع شكراً لك.\nمعلومات قيمة جداً، استمر.\nأحسنت النشر، موضوع مفيد.").split('\n')

# قائمة المقالات المستهدفة
target_urls = st.sidebar.text_area("روابط المقالات المستهدفة (URLs)").split('\n')
start_btn = st.sidebar.button("ابدأ النشر")

# --- المحرك ---
def post_comment(url, name, email, website, comment_text):
    with sync_playwright() as p:
        # تشغيل المتصفح (Headless أسرع)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            st.write(f"trying: {url}")
            page.goto(url, timeout=30000)
            
            # 1. البحث عن حقول الووردبريس القياسية
            # هذه المعرفات (Selectors) تعمل على 95% من مواقع ووردبريس
            page.fill('input[name="author"]', name)
            page.fill('input[name="email"]', email)
            page.fill('input[name="url"]', website)
            page.fill('textarea[name="comment"]', comment_text)
            
            # 2. الانتظار قليلاً لتبدو بشرياً
            time.sleep(random.uniform(2, 5))
            
            # 3. الضغط على زر الإرسال
            # زر الإرسال يختلف قليلاً لكن غالباً يحتوي على كلمة submit أو post
            try:
                page.click('input[name="submit"]')
            except:
                page.click('button[type="submit"]') # محاولة بديلة
                
            st.success(f"✅ تم نشر التعليق في: {url}")
            
        except Exception as e:
            st.error(f"❌ فشل في {url}: لم يتم العثور على صندوق التعليقات أو يوجد حماية.")
            
        finally:
            browser.close()

if start_btn:
    progress = st.progress(0)
    for i, url in enumerate(target_urls):
        if url.strip():
            # اختيار تعليق عشوائي من القائمة
            random_comment = random.choice(comments_list)
            post_comment(url.strip(), name, email, website, random_comment)
        progress.progress((i + 1) / len(target_urls))
