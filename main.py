import subprocess

from PyQt5 import QtWidgets
from PyQt5.QtCore import QT_VERSION_STR, QUrl, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QStyle
from PyQt5.QtWidgets import QFileDialog
from qfluentwidgets import Dialog, MessageBoxBase, SubtitleLabel, BodyLabel, HyperlinkLabel

from main_window import Ui_MainWindow
from common import *

# 软件版本
software_version = 1.1

# 资源文件访问
def packer_source_path(path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, path)

# 修改工作目录
cd = packer_source_path('')
os.chdir(cd)

# 资源文件索引路径
FRAMEWORK_RES_PATH = packer_source_path("framework-res.apk")
SIGN_KEY_PATH = packer_source_path("testkey.pk8")
SIGN_KEY_CERT_PATH = packer_source_path("testkey.x509.pem")

# 签名参数
SIGNER_PARAM = f"sign --key {SIGN_KEY_PATH} --cert {SIGN_KEY_CERT_PATH}"

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
        self.packer_thread = None

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
            err = Dialog("错误","请填写字体包名称,目标字体名,版本号和选择TTF文件", self)
            err.cancelButton.hide()
            err.exec_()
            return

        # 选择输出目录
        output_dir = QFileDialog.getExistingDirectory(self, "选择字体包输出目录")
        if not output_dir:
            return

        # 这里实现打包逻辑
        self.build_output.append(f"正在打包字体: {font_name}")
        self.build_output.append(f"TTF文件路径: {ttf_path}")
        self.build_output.append(f"输出目录: {output_dir}")

        self.packer_thread = PackerThread(font_name, ttf_path, ttf_filename, font_version, output_dir)
        self.packer_thread.progress_signal.connect(self.update_progress)
        self.packer_thread.finished_signal.connect(self.packing_finished)
        self.packer_thread.start()

        # 禁用打包按钮，防止重复点击
        self.btn_pack.setEnabled(False)

    def update_progress(self, message):
        self.build_output.append(message)

    def packing_finished(self, success, message):
        self.build_output.append(message)
        self.btn_pack.setEnabled(True)
        if success:
            pack_succ = Dialog("打包完成", "字体包打包成功！", self)
            pack_succ.cancelButton.hide()
            pack_succ.exec_()
        else:
            pack_err = Dialog("打包失败", message, self)
            pack_err.cancelButton.hide()
            pack_err.exec_()

    def clear_textOutput(self):
        self.build_output.clear()

    def open_workspace(self):
        work_dir = os.path.abspath(os.path.dirname(__file__))
        if sys.platform.startswith("win32"):
            # Windows打开当前文件目录
            os.startfile(work_dir)  # 在Windows上打开文件夹
        elif sys.platform.startswith("darwin"):
            # MacOS打开目录
            subprocess.call(["open", work_dir])
        elif sys.platform.startswith("linux"):
            #Linux打开目录
            subprocess.Popen(['xdg-open', work_dir])

    def show_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def show_aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self,"关于Qt")

# 关于对话框
class AboutDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.titleLabel = SubtitleLabel()
        self.titleLabel.setText("关于")

        self.contentLabel = BodyLabel()
        self.contentLabel.setText(f"Motorola Font Packer\n"
                           f"一款简单的摩托罗拉手机MyUI字体包打包器\n"
                           f"作者: Yuyuko1024\n")
        self.contentLabel.setOpenExternalLinks(True)

        self.linkLabel = (
            HyperlinkLabel(QUrl("https://github.com/Yuyuko1024/Motorola-Fonts-Packer"),
                           '点击前往 GitHub'))
        self.linkLabel.setUnderlineVisible(True)

        self.version_label = BodyLabel()
        self.version_label.setText(f"版本: {software_version}")

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.contentLabel)
        self.viewLayout.addWidget(self.linkLabel)
        self.viewLayout.addWidget(self.version_label)
        self.cancelButton.hide()
        #self.widget.setMinimumSize(350)

# 打包器线程
class PackerThread(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, font_name, ttf_path, ttf_filename, pkg_version, output_dir):
        super().__init__()
        self.font_name = font_name
        self.ttf_path = ttf_path
        self.ttf_filename = ttf_filename
        self.pkg_version = pkg_version
        self.output_dir = output_dir
        self.packer = Packer(self)

    def run(self):
        try:
            self.packer.pack_font(self.font_name, self.ttf_path, self.ttf_filename, self.pkg_version,
                                  self.output_dir)
            self.finished_signal.emit(True, "打包完成")
        except Exception as e:
            self.finished_signal.emit(False, f"打包失败: {str(e)}")

    def print_output(self, message):
        self.progress_signal.emit(message)

#打包器主类
class Packer:
    def __init__(self, thread):
        self.thread = thread

    def print_output(self, message):
        self.thread.print_output(message)

    def pack_font(self, font_name, ttf_path, ttf_filename, pkg_version, output_dir):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.print_output(f"创建临时工作目录: {temp_dir}")

            # 复制模板文件夹到临时目录
            template_dir = packer_source_path("motorola-fonts-template")
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
            self.pack_main(work_dir, output_apk)

    @staticmethod
    def replace_in_file(file_path, old_string, new_string):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        content = content.replace(old_string, new_string)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def pack_main(self, src, out):
        check_file(src)
        if os.path.exists(out):
            remove_path(out)
        appTmp = tempfile.mkdtemp("", "ThemeMaker_")
        self.print_output("复制文件...")
        remove_path(appTmp)
        dir2dir(src, appTmp)
        self.print_output("打包中...")
        self.doAAPT(appTmp, os.path.join(appTmp, "raw.apk"), [FRAMEWORK_RES_PATH])  # 使用FRAMEWORK_RES_PATH
        self.doZipAlign(os.path.join(appTmp, "raw.apk"), out)
        self.signAPK(out)
        self.print_output("完成！")
        ##打包完成后清理现场
        remove_path(appTmp)

    def doAAPT(self, src, out, resapk):
        self.print_output("执行AAPT操作...")
        androidManifestFile = os.path.join(src, "AndroidManifest.xml")
        check_file(androidManifestFile)
        cmd = [get_bin("aapt"), "p", "-M", androidManifestFile]

        assetsFile = os.path.join(src, "assets")
        if os.path.exists(assetsFile):
            cmd.extend(["-A", assetsFile])

        resFile = os.path.join(src, "res")
        if os.path.exists(resFile):
            cmd.extend(["-S", resFile])

        for res in resapk:
            cmd.extend(["-I", res])

        cmd.extend(["-F", out])

        result = self.run_command(cmd)
        if result['returncode'] != 0:
            raise Exception(f"AAPT 执行失败:\n {result['stderr']}")

    def doZipAlign(self, src, out):
        self.print_output("执行ZipAlign...")
        cmd = [get_bin("zipalign"), "4", src, out]
        result = self.run_command(cmd)
        if result['returncode'] != 0:
            raise Exception(f"ZipAlign 执行失败:\n {result['stderr']}")

    def signAPK(self, src):
        self.print_output("签名APK...")
        ext = ".bat" if is_win() else ""
        cmd = [get_bin("apksigner", ext=ext)] + SIGNER_PARAM.split() + [src]
        result = self.run_command(cmd)
        if result['returncode'] != 0:
            raise Exception(f"APK 签名失败:\n {result['stderr']}")

    def run_command(self, cmd):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        returncode = process.returncode

        if stdout:
            self.print_output(stdout)
        if stderr:
            self.print_output(stderr)

        return {
            'stdout': stdout,
            'stderr': stderr,
            'returncode': returncode
        }

# main方法
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

