import os
from playwright.sync_api import sync_playwright

OUT = r"C:\Users\saadb\Downloads\MiniProjet\screenshots"
os.makedirs(OUT, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BASE = "http://127.0.0.1:8000"

def shot(page, name):
    path = os.path.join(OUT, f"{name}.png")
    page.screenshot(path=path, full_page=True)
    print(f"  saved: {name}.png")

def logout(page):
    page.evaluate("""() => {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/accounts/logout/';
        const csrf = document.createElement('input');
        csrf.name = 'csrfmiddlewaretoken';
        csrf.value = document.cookie.split('csrftoken=')[1]?.split(';')[0] || '';
        form.appendChild(csrf);
        document.body.appendChild(form);
        form.submit();
    }""")
    page.wait_for_url(BASE + "/")

def login(page, username, password):
    page.goto(BASE + "/accounts/login/")
    page.fill("input[name=username]", username)
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")
    page.wait_for_load_state("networkidle")

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=EDGE,
        headless=True,
        args=["--no-sandbox"]
    )
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    # 1-3 already done, just redo quickly
    page.goto(BASE + "/")
    page.wait_for_load_state("networkidle")
    shot(page, "01_home")

    page.goto(BASE + "/accounts/login/")
    page.wait_for_load_state("networkidle")
    shot(page, "02_login")

    page.goto(BASE + "/register/")
    page.wait_for_load_state("networkidle")
    shot(page, "03_register")

    # Admin
    login(page, "admin", "admin123")
    shot(page, "04_admin_dashboard")

    page.goto(BASE + "/dashboard/admin/users/")
    page.wait_for_load_state("networkidle")
    shot(page, "05_admin_users")

    page.goto(BASE + "/dashboard/admin/modules/")
    page.wait_for_load_state("networkidle")
    shot(page, "06_admin_modules")

    logout(page)

    # Teacher
    login(page, "sara", "sara123")
    shot(page, "07_enseignant_dashboard")

    first_link = page.query_selector("a[href*='/seance/'][href*='/dashboard/']")
    if first_link:
        href = first_link.get_attribute("href")
        if "delete" not in href and "export" not in href:
            page.goto(BASE + href)
            page.wait_for_load_state("networkidle")
            shot(page, "08_mark_attendance")

    logout(page)

    # Student
    login(page, "etud1", "etud123")
    shot(page, "09_etudiant_dashboard")

    browser.close()
    print("\nAll screenshots saved to:", OUT)
