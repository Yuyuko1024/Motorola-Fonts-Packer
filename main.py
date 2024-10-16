from PyQt5 import QtWidgets, Qt
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QStyle, QDialog, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QFileDialog
from main_window import Ui_MainWindow
from common import *

# 软件版本
software_version = 1.0
# 签名参数
SIGNER_PARAM = "sign --key testkey.pk8 --cert testkey.x509.pem"

# 添加 Qt 插件路径到环境变量
if hasattr(sys, 'frozen'):
    # 如果是打包后的可执行文件
    qt_plugin_path = os.path.join(sys._MEIPASS, 'PyQt5', 'Qt', 'plugins')
else:
    # 如果是 Python 脚本
    qt_plugin_path = os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages', 'PyQt5', 'Qt', 'plugins')

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path

# 主程序的功能
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.packer = Packer(self.build_output)

        # 连接信号和槽
        self.btn_choose_file.clicked.connect(self.choose_file)
        self.btn_pack.clicked.connect(self.pack_font)
        self.btn_clear.clicked.connect(self.clear_textOutput)
        self.action_open_workspace.triggered.connect(self.open_workspace)
        self.action_about.triggered.connect(self.show_about)
        self.action_Qt.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMenuButton))
        self.action_Qt.triggered.connect(self.show_aboutQt)
        self.edit_font_name.setToolTip("字体包名称，将会作为安装字体包时显示的名称。")
        self.edit_font_target_name.setToolTip("在Motorola手机的字体选择界面显示的字体名称，不可以包含中文和空格以及任何符号。")
        self.edit_pkg_version.setToolTip("字体包版本号，将会作为安装字体包时显示的版本号。")
        self.edit_pkg_version.setText("1.0")
        self.print_sysinfo()

    def print_sysinfo(self):
        py_version = sys.version
        self.build_output.append(f"PyQt版本： {QT_VERSION_STR}")
        self.build_output.append(f"Qt 插件路径: {qt_plugin_path}")
        self.build_output.append(f"Python 版本: {py_version}")
        self.build_output.append(f"软件版本: {software_version}")

    def choose_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择TTF文件", "", "TTF Files (*.ttf)")
        if file_name:
            self.edit_ttf_path.setText(file_name)

    def pack_font(self):
        font_name = self.edit_font_name.text()
        ttf_path = self.edit_ttf_path.text()
        ttf_filename = self.edit_font_target_name.text()
        font_version = self.edit_pkg_version.text()
        if not font_name or not ttf_path or not ttf_filename or not font_version:
            self.build_output.append("错误: 请填写字体包名称,目标字体名,版本号和选择TTF文件")
            QtWidgets.QMessageBox.critical(self, "错误","请填写字体包名称,目标字体名,版本号和选择TTF文件")
            return

        # 选择输出目录
        output_dir = QFileDialog.getExistingDirectory(self, "选择字体包输出目录")
        if not output_dir:
            return

        # 这里实现打包逻辑
        self.build_output.append(f"正在打包字体: {font_name}")
        self.build_output.append(f"TTF文件路径: {ttf_path}")
        self.build_output.append(f"输出目录: {output_dir}")

        try:
            self.packer.pack_font(font_name, ttf_path, ttf_filename, font_version, output_dir)
            self.build_output.append("打包完成")
        except Exception as e:
            self.build_output.append(f"打包失败: {str(e)}")

    def clear_textOutput(self):
        self.build_output.clear()

    def open_workspace(self):
        # 打开当前文件目录
        os.startfile(os.path.abspath(os.path.dirname(__file__)))  # 在Windows上打开文件夹

    def show_about(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()

    def show_aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self,"关于Qt")

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("关于")
        layout = QVBoxLayout()

        label = QLabel()
        about_text = """
        <p>Motorola Font Packer</p>
        <p>一款简单的摩托罗拉手机MyUI字体包打包器</p>
        <p>GitHub: <a href="https://github.com/Yuyuko1024/Motorola-Fonts-Packer">https://github.com/Yuyuko1024/Motorola-Fonts-Packer</a></p>
        <p>作者: Yuyuko1024</p>
        """
        label.setText(about_text)
        label.setOpenExternalLinks(True)

        version_label = QLabel()
        version_label.setText(f"版本: {software_version}")

        layout.addWidget(label)
        layout.addWidget(version_label)
        self.setLayout(layout)

class Packer:
    def __init__(self, output_widget):
        self.output_widget = output_widget

    def print_output(self, message):
        self.output_widget.append(message)

    def pack_font(self, font_name, ttf_path, ttf_filename, pkg_version, output_dir):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.print_output(f"创建临时工作目录: {temp_dir}")

            # 复制模板文件夹到临时目录
            template_dir = os.path.join(os.path.dirname(__file__), "motorola-fonts-template")
            work_dir = os.path.join(temp_dir, "motorola-fonts-template")
            shutil.copytree(template_dir, work_dir)

            # 复制TTF文件到assets/fonts目录
            fonts_dir = os.path.join(work_dir, "assets", "fonts")
            os.makedirs(fonts_dir, exist_ok=True)
            target_ttf_path = os.path.join(fonts_dir, f"{ttf_filename}.ttf")
            shutil.copy(ttf_path, target_ttf_path)

            # 替换strings.xml中的字体名称
            self.replace_in_file(os.path.join(work_dir, "res", "values", "strings.xml"),
                                 "{packer.fontName}", font_name)

            # 生成包名并替换AndroidManifest.xml中的包名
            package_name = f"org.motofonts.font.{ttf_filename}"
            self.replace_in_file(os.path.join(work_dir, "AndroidManifest.xml"),
                                 "{packer.fontPkgName}", package_name)
            self.replace_in_file(os.path.join(work_dir, "AndroidManifest.xml"),
                                 "{packer.fontVersion}", pkg_version)

            # 执行打包操作
            output_apk = os.path.join(output_dir, f"{font_name}.apk")
            self.pack_main(work_dir, output_apk, ["framework-res.apk"])

    @staticmethod
    def replace_in_file(file_path, old_string, new_string):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        content = content.replace(old_string, new_string)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def pack_main(self, src, out, resapk):
        check_file(src)
        if os.path.exists(out):
            remove_path(out)
        appTmp = tempfile.mkdtemp("", "ThemeMaker_")
        self.output_widget.append("复制文件...")
        remove_path(appTmp)
        dir2dir(src, appTmp)
        self.output_widget.append("打包中...")
        self.doAAPT(appTmp, os.path.join(appTmp, "raw.apk"), resapk)
        self.doZipAlign(os.path.join(appTmp, "raw.apk"), out)
        self.signAPK(out)
        self.output_widget.append("完成！")

    def doAAPT(self, src, out, resapk):
        self.print_output("执行AAPT操作...")
        androidManifestFile = os.path.join(src, "AndroidManifest.xml")
        check_file(androidManifestFile)
        cmd = " -M \"" + androidManifestFile + "\""
        assetsFile = os.path.join(src, "assets")
        if (os.path.exists(assetsFile)):
            cmd += " -A " + "\"" + assetsFile + "\""
        resFile = os.path.join(src, "res")
        if (os.path.exists(resFile)):
            cmd += " -S " + "\"" + resFile + "\""
        for res in resapk:
            cmd += " -I " + "\"" + res + "\""
        cmd += " -F " + "\"" + out + "\""
        os.system(" ".join((get_bin("aapt"), "p", cmd)))

    def doZipAlign(self, src, out):
        self.print_output("执行ZipAlign...")
        os.system(" ".join((get_bin("zipalign"), "4", "\"" + src + "\"", "\"" + out + "\"")))

    def signAPK(self, src):
        self.print_output("签名APK...")
        if is_win():
            ext = ".bat"
        else:
            ext = ""
        os.system(" ".join((get_bin("apksigner", ext=ext), SIGNER_PARAM, "\"" + src + "\"")))


if __name__ == '__main__':
    print("PyQt5 version:",QT_VERSION_STR)
    print("Qt plugin path:", qt_plugin_path)
    print("Python version:", sys.version)
    print("Software version", software_version)
    app = QApplication(sys.argv)
    window = MainWindow()
    # 强制固定使用800x500
    window.setFixedSize(800, 520)
    window.show()
    sys.exit(app.exec_())

