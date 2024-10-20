import sys

from DrissionPage import Chromium

from DrissionPage import ChromiumOptions


opt = ChromiumOptions(read_file=False)

if sys.platform.startswith('linux'):
    opt.set_browser_path('/opt/google/chrome/google-chrome')  # 设置路径
opt.no_imgs(True).mute(True)  # 不加载图片 并 静音
# opt.incognito()  # 匿名模式
opt.headless()  # 无头模式
opt.set_user_agent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/124.0.0.0 Safari/537.36 PTST/240508.140043')
opt.set_argument('--no-sandbox')  # 无沙盒模式
opt.set_local_port(9222)

chrome = Chromium(addr_or_opts=opt)

chrome.quit()

