import streamlit as st
import openai

st.set_page_config(page_title="MetaDef CT - עוזר פרוטוקולי CT", page_icon="🧠")

st.title("🧠 MetaDef CT")
st.markdown("עוזר אישי לרדיולוגים לבחירת פרוטוקול CT לפי שאלה קלינית")

# Load API key securely from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# File references for display
st.markdown("🔗 **הקבצים שעליהם מבוססת האפליקציה:**")
st.markdown("- פרוטוקולים סיטי בטן 2024-02")
st.markdown("- פרוטוקולים נפוצים")
st.markdown("- קובץ Padlet")

# Clinical input
clinical_question = st.text_area("📝 הזן שאלה קלינית בעברית", height=150)

if st.button("📡 שלח וקבל פרוטוקול"):
    if not clinical_question.strip():
        st.warning("יש להזין שאלה קלינית.")
    else:
        # System prompt (same as original)
        system_prompt = """אתה GPT עוזר אישי לרדיולוגים לקביעת פרוטוקולי CT מדויקים לפי שאלה קלינית.
אתה פועל בעברית בלבד, ומסתמך על שלושה מסמכים מקצועיים:
1. חוברת “פרוטוקולים סיטי בטן 2024-02”
2. קובץ “פרוטוקולים נפוצים”
3. קובץ “Padlet”

🔹 כל השימוש הוא דמיוני בלבד, לצורך הדרכה ולמידה בלבד, ואינו מחליף שיקול דעת רפואי.

🟦 מבנה התשובה:
• שם פרוטוקול מלא
• קיצור (למשל: בטן 2, מוח 1, חזה 4)
• אזור הסריקה (בטן / חזה / נוירולוגי / אורתופדי / ילדים)
• חומר ניגוד פומי – כן / לא
• סריקה מאוחרת – כן / לא
• חומר ניגוד ורידי – כן / לא + כמות
• דחיפות – שגרתי / דחוף לפי קליניקה
• שלבי סריקה עיקריים בלבד – כגון: ללא ניגוד, פורטלי, עורקי, מאוחר 5 דק’ (אין לכלול SURVIEW או Locator)
• הערות קליניות חשובות

🔴 חובה לברר גיל ומאפיינים קליניים לפני המלצה. יש לעצור ולשאול אם חסר מידע.

❗ חובה לעיין בקובץ Padlet לפני המלצה — ייתכנו שלבים מיוחדים, שתייה, שינויים בטכניקה, מגבלות ועוד.

הקפד על שפה רפואית מקצועית ומונחים מדויקים (שלב פורטלי / ללא חומר ניגוד / מאוחר 5 דק’).
"""

        user_prompt = f"שאלה קלינית: {clinical_question.strip()}"

        # Call OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.4
            )
            reply = response['choices'][0]['message']['content']
            st.markdown("### 📋 תשובת GPT:")
            st.markdown(reply)
        except Exception as e:
            st.error(f"שגיאה: {str(e)}")