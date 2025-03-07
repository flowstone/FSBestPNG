from fs_base.const.app_constants import AppConstants


class FsConstants(AppConstants):
    """
    ---------------------
    宽度为0 高度为0,则表示窗口【宽高】由组件们决定
    ---------------------
    """
    # 主窗口相关常量
    APP_WINDOW_WIDTH = 300
    APP_WINDOW_HEIGHT = 300
    APP_WINDOW_TITLE = "FSBestPNG"
    VERSION = "0.1.1"
    COPYRIGHT_INFO = f"© 2025 {APP_WINDOW_TITLE}"
    # 悬浮球相关常量
    APP_MINI_SIZE = 80
    APP_MINI_WINDOW_TITLE = ""



    WINDOW_TITLE_IMAGE_TOOL = "图片工具"


    # 共用的常量，应用图标
    APP_ICON_FULL_PATH = "resources/images/app.ico"
    APP_MINI_ICON_FULL_PATH = "resources/images/app_mini.ico"
    APP_BAR_ICON_FULL_PATH = "resources/images/app_bar.ico"
    UPLOAD_IMAGE_FULL_PATH = "resources/images/upload.svg"

    PROJECT_ADDRESS = "https://github.com/flowstone/FSBestPNG"
    BASE_QSS_PATH = "resources/qss/base.qss"
    LICENSE_FILE_PATH = "resources/txt/LICENSE"




    # 保存文件路径
    AppConstants.SAVE_FILE_PATH_WIN = "C:\\FSBestPNG\\"
    AppConstants.SAVE_FILE_PATH_MAC = "~/FSBestPNG/"
    EXTERNAL_APP_INI_FILE = "app.ini"

    APP_INI_FILE = "app.ini"
    HELP_PDF_FILE_PATH = "resources/pdf/help.pdf"
    FONT_FILE_PATH = "resources/fonts/AlimamaFangYuanTiVF-Thin.ttf"

    #首选项
    PREFERENCES_WINDOW_TITLE = "首选项"
    PREFERENCES_WINDOW_TITLE_ABOUT = "关于"
    PREFERENCES_WINDOW_TITLE_GENERAL = "常规"
