import os, sys
os.environ["PLAYWRIGHT_BROWSERS_PATH"]="/opt/pw-browsers"
from playwright.sync_api import sync_playwright
SP="/tmp/claude-0/-home-user-Brandons-Jewlwery-Site-/c22e2c9b-8847-5b38-a2b8-5d4f48054a32/scratchpad"
URL="file:///home/user/Brandons-Jewlwery-Site-/index.html"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    pg=b.new_page(viewport={"width":1440,"height":950}, device_scale_factor=1)
    errs=[]
    pg.on("console", lambda m: errs.append(m.type+": "+m.text) if m.type=="error" else None)
    pg.on("pageerror", lambda e: errs.append("pageerror: "+str(e)))
    pg.goto(URL); pg.wait_for_timeout(600)
    pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
    pg.wait_for_timeout(900)
    # trigger all reveals
    pg.evaluate("""async()=>{const h=document.body.scrollHeight;for(let y=0;y<h;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,60));}window.scrollTo(0,0);}""")
    pg.evaluate("document.querySelectorAll('.rv,.rv-img,.rv-line').forEach(e=>e.classList.add('is-in'))")
    pg.wait_for_timeout(1600)
    pg.screenshot(path=SP+"/full.png", full_page=True)
    pg.set_viewport_size({"width":390,"height":844})
    pg.wait_for_timeout(800)
    pg.evaluate("""async()=>{const h=document.body.scrollHeight;for(let y=0;y<h;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,50));}window.scrollTo(0,0);}""")
    pg.evaluate("document.querySelectorAll('.rv,.rv-img,.rv-line').forEach(e=>e.classList.add('is-in'))")
    pg.wait_for_timeout(1600)
    pg.screenshot(path=SP+"/mobile.png", full_page=True)
    print("CONSOLE:", errs if errs else "clean")
    b.close()
