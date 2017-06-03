# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QColor, QFont, QApplication, QFontMetrics
from PyQt4.Qsci import QsciLexerCustom, QsciScintilla

class OrLexer(QsciLexerCustom):
        def __init__(self, parent):
                QsciLexerCustom.__init__(self, parent)
                self._styles = {
                        0: 'Default',
                        1: 'Comment_Start',
                        2: 'Comment',
                        3: 'Comment_End'
                        }
                for key, value in self._styles.items():
                        setattr(self, value, key)
                self._foldcompact = True

        def foldCompact(self):
                return self._foldcompact

        def setFoldCompact(self, enable):
                self._foldcompact = bool(enable)

        def language(self):
                return 'Config Files'

        def description(self, style):
                return self._styles.get(style, '')

        def defaultColor(self, style):
                if style == self.Default:
                        return QColor('#000000')
                elif style == self.Comment:
                        return QColor('#228B22')
                return QsciLexerCustom.defaultColor(self, style)

        def defaultFont(self, style):
                if style == self.Comment:
                    return QFont('Courier', 10, QFont.Light)
                elif style == self.Default:
                    return QFont('Courier', 10, QFont.Normal)
                return QsciLexerCustom.defaultFont(self, style)


        def defaultEolFill(self, style):
                # This allowed to colorize all the background of a line.
                if style == self.Comment or style == self.Comment_End or style == self.Comment_Start:
                        return True
                return QsciLexerCustom.defaultEolFill(self, style)

        def styleText(self, start, end):
                editor = self.editor()
                if editor is None:
                        return
                SCI = editor.SendScintilla
                source = ''
                if end > editor.length():
                        end = editor.length()
                if end > start:
                        source = bytearray(end - start)
                        SCI(QsciScintilla.SCI_GETTEXTRANGE, start, end, source)
                if not source:
                        return

                index = SCI(QsciScintilla.SCI_LINEFROMPOSITION, start)
                if index > 0:
                        pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index - 1)
                        state = SCI(QsciScintilla.SCI_GETSTYLEAT, pos)
                else:
                        state = self.Default
                self.startStyling(start, 0x1f)
                for line in source.splitlines(True):
                        try:
                            line = line.decode('utf-8', 'ignore')
                        except AttributeError:
                            pass
                        length = len(line)
                        if line.startswith('#'):
                            state = self.Comment
                        else:
                            state = self.Default
                        self.setStyling(length, state)

#            
class OrSciScintilla(QsciScintilla):
    ARROW_MARKER_NUM = 1
    REC_MARKER_NUM = 2
    
    def __init__(self, parent = None):
        QsciScintilla.__init__(self, parent)
        self.setup()
        
    def paste(self):
        QsciScintilla.paste(self)
        self.emit(SIGNAL('paste'))
                
    def setup(self):
        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width('0000'))
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor('#cccccc'))
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightTriangle, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor('#ee1111'), self.ARROW_MARKER_NUM)
        self.markerDefine(QsciScintilla.Circle, self.REC_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor('#87CEEB'), self.REC_MARKER_NUM)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor('#FFA07A'))
        self.my_lexer = OrLexer(self)
        self.setLexer(self.my_lexer)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.tracking_marker = None
        
    def on_margin_clicked(self, nmargin, nline, modifiers):
        """Toggle marker for the line the margin was clicked on"""
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.REC_MARKER_NUM)
        else:
            self.markerAdd(nline, self.REC_MARKER_NUM)

    def set_tracking_mark(self, nline):
        if self.tracking_marker:
            self.markerDeleteHandle(self.tracking_marker)
        self.tracking_marker = self.markerAdd(nline, self.ARROW_MARKER_NUM)
    
    def cursor_next_line(self):
        lin, _ = self.getCursorPosition()
        self.setCursorPosition(lin + 1, 0)
        
    def get_current_line(self):
        return self.text(self.getCursorPosition()[0])
    
    def getLineNumber(self):
        lin, _ = self.getCursorPosition()
        return lin + 1

        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    text = OrSciScintilla()
    text.setText('# It works!\nnew line ')
    text.set_tracking_marker(1)
    text.set_tracking_marker(0)
    print(text.markerLine(text.REC_MARKER_NUM))
    text.show()
    app.exec_()
