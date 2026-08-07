import os
os.environ["PLAYWRIGHT_BROWSERS_PATH"]="/opt/pw-browsers"
from playwright.sync_api import sync_playwright
SP="/tmp/claude-0/-home-user-Brandons-Jewlwery-Site-/c22e2c9b-8847-5b38-a2b8-5d4f48054a32/scratchpad"
URL="file:///home/user/Brandons-Jewlwery-Site-/index.html"
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    pg=b.new_page(viewport={"width":1440,"height":900})
    pg.on("pageerror", lambda e: errs.append("pageerror: "+str(e)))
    pg.on("console", lambda m: errs.append(m.type+": "+m.text) if m.type=="error" and "fonts" not in m.text else None)
    pg.goto(URL); pg.wait_for_timeout(700)

    # quick view on the third product
    pg.evaluate("document.querySelector('#featured').scrollIntoView()"); pg.wait_for_timeout(700)
    pg.eval_on_selector_all('.card', "els=>els.forEach(e=>e.classList.add('is-in'))")
    pg.locator('.card[data-id=p3] [data-quick]').click(force=True); pg.wait_for_timeout(900)
    pg.screenshot(path=SP+"/s_qv.png")

    # add to bag -> cart drawer
    pg.locator('[data-qv-add]').click(); pg.wait_for_timeout(900)
    pg.screenshot(path=SP+"/s_cart.png")
    cart_count = pg.locator('[data-cart-count]').first.inner_text()
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)

    # wishlist toggle then panel
    pg.locator('.card[data-id=p1] [data-wish]').click(force=True); pg.wait_for_timeout(300)
    wish_count = pg.locator('[data-wish-count]').first.inner_text()

    # filter
    pg.locator('[data-filter=watches]').click(); pg.wait_for_timeout(600)
    visible = pg.eval_on_selector_all('.card', "els=>els.filter(e=>!e.hidden).length")
    pg.locator('[data-filter=all]').click(); pg.wait_for_timeout(300)

    # search
    pg.locator('[data-open=search]').click(); pg.wait_for_timeout(600)
    pg.fill('[data-search-input]', 'watch'); pg.wait_for_timeout(500)
    pg.screenshot(path=SP+"/s_search.png")
    hits = pg.eval_on_selector_all('[data-search-list] li', "e=>e.length")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)

    # mega menu
    pg.mouse.move(120, 60); pg.hover('.nav__item[data-mega] .nav__link'); pg.wait_for_timeout(700)
    pg.screenshot(path=SP+"/s_mega.png", clip={"x":0,"y":0,"width":900,"height":560})

    # mobile nav
    pg.set_viewport_size({"width":390,"height":844}); pg.wait_for_timeout(400)
    pg.locator('[data-open=mnav]').click(); pg.wait_for_timeout(800)
    pg.screenshot(path=SP+"/s_mnav.png")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)

    # persistence across reload
    pg.reload(); pg.wait_for_timeout(800)
    persisted = pg.locator('[data-cart-count]').first.inner_text()

    print("cart:",cart_count,"wish:",wish_count,"watch-filter visible:",visible,"search hits:",hits,"persisted cart:",persisted)
    print("ERRORS:", errs if errs else "none")
    b.close()
