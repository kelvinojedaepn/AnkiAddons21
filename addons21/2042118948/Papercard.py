#!/usr/bin/env python3

# Copyright: Tobias Haupenthal
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
###############################################################################
"""
This plugin exports all flashcards to pdf.
It adds a

Configuration
----------
This a plugin, which can export anki vocabulary cards to a HTML or PDF page.
You can use it to print them on paper.
"""

import base64
import logging
import re
import subprocess
import sys
import time
from os import environ
from pathlib import Path
from string import Template

# noinspection PyUnresolvedReferences
from PyQt5.QtCore import QStandardPaths

# from .types import AnkiUtils, Config, Cards

###############################################################################
# Configuration
#


cssStyle = '''
@page {
    size: ${papersize} ${orientation};
    margin: 0
}

@media print {
    @page {size: ${papersize} ${orientation}; margin: 0};
}

html, body, .pageA, .pageB {
    height: 100%;
    width: 100%;
    margin: 0;
}

body {
    font-size: 100%;
    font-family: Liberation Sans, sans;
}

.pageA, .pageB {
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    page-break-after:always;
}

.pageB {
    flex-direction: row-reverse;
}

.cardA, .cardB {
    box-sizing: border-box;
    overflow: hidden;
    width: ${cardWidth};
    height: ${cardHeight};
    padding: ${cardPadding};
}

.cardA {
    border-bottom: dashed 1px grey;
    border-right: dashed 1px grey;
}

img {
    max-width: 100%;
    max-height: 100%;
}
'''

htmlTemplate = '''<!DOCTYPE html>
<html>
<head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<style>
${style}
</style></head>
<body>
${content}
</body>
</html>
'''

###############################################################################
# Main Program
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class IntendedException(Exception):
    pass


class Papercard:
    instance = None

    def __init__(self, ankiutils, addonmanager, mediapath: Path):
        self.ankiutils = ankiutils
        self.addonmanager = addonmanager
        self.mediapath = mediapath
        self.config = None
        self.wkhtmltopdf = None
        self.htmlout = None
        self.pdfout = None

    def get_outputdir(self) -> Path:
        path = self.config['output']['path']
        if path == 'download':
            return Path(QStandardPaths.writableLocation(QStandardPaths.DownloadLocation))

        return self.get_homepath(path)

    @staticmethod
    def get_homepath(path: str) -> Path:
        path = Path(path)
        if not path.is_absolute():
            return Path.home() / path.as_posix()

        return path.absolute()

    def build_question_card(self, q: str) -> str:
        # logging.debug("build question")
        if self.config['card']['plaintext']:
            q = re.sub('<style>[^<]*</style>', '', q)
        q = re.sub('(<img.*? src=")(.*?)(".*?>)', self.replace_image_source, q)
        html = '<div class="cardA">{}</div>\n'.format(q)
        return html

    def build_answer_card(self, a: str) -> str:
        # logging.debug("build answer")
        if not self.config['card']['repeatQuestionOnAnswer']:
            a = a.split('<hr id=answer>')[-1].strip()
        if self.config['card']['plaintext']:
            a = re.sub('<style>[^<]*</style>', '', a)
        a = re.sub('(<img.*? src=")(.*?)(".*?>)', self.replace_image_source, a)
        html = '<div class="cardB">{}</div>\n'.format(a)
        return html

    @staticmethod
    def replace_image_source(match) -> str:
        imagefile = Path(match.group(2))
        if imagefile.exists():
            ext = imagefile.suffix[1:]
            encoded_string = base64.b64encode(imagefile.read_bytes())
            img_binary = '{}data:image/{};base64,{}{}' \
                .format(match.group(1), ext, encoded_string.decode('ascii'), match.group(3))
        else:
            img_binary = match.group(0)
        return img_binary

    def prepare_html(self, content: str) -> str:
        settings = {
            'papersize': self.config['paper']['format'],
            'orientation': self.config['paper']['orientation'],
            'cardWidth': str(100 / self.config['paper']['cardsPerRow']) + '%',
            'cardHeight': str(100 / self.config['paper']['cardsPerCol']) + '%',
            'cardPadding': str(100 / self.config['card']['padding']) + '%',
        }
        style = Template(cssStyle).substitute(settings)
        html = Template(htmlTemplate).substitute({'style': style, 'content': content})
        return html

    def arrange_cards(self, cards) -> str:
        questions, answers = cards
        cards_per_page = self.config['paper']['cardsPerRow'] * self.config['paper']['cardsPerCol']
        html = ''
        i = j = 0
        while True:
            html += '<div class="pageA">\n'
            while i < len(questions):
                html += self.build_question_card(questions[i])
                i += 1
                if i % cards_per_page == 0:
                    break
            html += '</div><div class="pageB">\n'
            while j < len(answers):
                html += self.build_answer_card(answers[j])
                j += 1
                if j % cards_per_page == 0:
                    break
            html += '</div>'
            if j == len(answers):
                break
        return html

    def save_html(self, deck: str, content: str) -> Path:
        deck = deck.replace(':', '^')
        filename = self.config['output']['filename'].replace('{deck}', deck)
        timestamp = time.strftime(self.config['output']['filedate'])
        file = self.get_outputdir() / (filename + timestamp + '.html')
        try:
            file.write_text(content, encoding='utf8')
        except (OSError, IOError) as e:
            error = 'HTML file saving failed: {}.\n Does the path "{}" really exists?'.format(e, file)
            logging.error(error)
            raise IntendedException(error)
        return file

    def find_wkhtmltopdf(self):
        if 'wkhtmltopdfPath' in self.config['output'] and self.config['output']['wkhtmltopdfPath']:
            path = self.get_homepath(self.config['output']['wkhtmltopdfPath'])
            if path.is_file():
                return path
        if sys.platform == 'linux' or sys.platform == 'darwin':
            call = subprocess.run(['which', 'wkhtmltopdf'], encoding='utf8', stdout=subprocess.PIPE)
            if call.returncode == 0:
                path = Path(call.stdout.strip())
                if path.exists():
                    return path
        elif sys.platform == 'win32' or sys.platform == 'cygwin':
            call = subprocess.run(['where', 'wkhtmltopdf'], encoding='utf8', stdout=subprocess.PIPE)
            if call.returncode == 0:
                path = Path(call.stdout.strip())
                if path.exists():
                    return path
            if 'ProgramW6432' in environ:
                path = Path(environ['ProgramW6432']) / 'wkhtmltopdf/bin/wkhtmltopdf.exe'
                if path.exists():
                    return path
            if 'ProgramFiles(x86)' in environ:
                path = Path(environ['ProgramFiles(x86)']) / 'wkhtmltopdf/bin/wkhtmltopdf.exe'
                if path.exists():
                    return path
        return None

    def get_wkhtmltopdf_cmd(self):
        if self.wkhtmltopdf:
            return self.wkhtmltopdf
        cmd = self.find_wkhtmltopdf()

        if not cmd:
            error = 'Cannot find command wkhtmltopdf.<br/>' + \
                    'Either install <a href="https://wkhtmltopdf.org">wkhtmltopdf</a><br/>' + \
                    ' or switch off PDF generation in Anki\'s plugin config (Tools -> Add-ons) '
            logging.error(error)
            raise IntendedException(error)
        self.wkhtmltopdf = cmd
        return cmd

    def generate_pdf(self, htmlfile: Path):
        if not self.config['output']['createPdf']:
            return
        if htmlfile is None or not htmlfile.exists():
            error = 'HTML file has not been generated. It is required for the pdf generation step.'
            logging.error(error)
            raise IntendedException(error)

        # generate pdf
        pdffile = htmlfile.parent / (htmlfile.stem + '.pdf')
        m = str(0)
        pdf_options = ['--orientation', self.config['paper']['orientation'],
                       '--margin-top', m, '--margin-right', m, '--margin-bottom', m, '--margin-left', m]
        files = [str(htmlfile), str(pdffile)]
        cmd = [str(self.get_wkhtmltopdf_cmd().absolute())]

        try:
            subprocess.run(cmd + pdf_options + files, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                           encoding='utf8')
        except Exception as e:
            error = 'PDF generation failed with an error: {}'.format(e)
            logging.error(error)
            raise IntendedException(error)

        return pdffile

    def generate_paper(self, deckname, cards):
        content = self.arrange_cards(cards)
        html = self.prepare_html(content)
        htmlfile = self.save_html(deckname, html)
        pdffile = self.generate_pdf(htmlfile)

        if not self.config['output']['createHtml'] and htmlfile.exists():
            htmlfile.unlink()
            htmlfile = None

        return htmlfile, pdffile

    @staticmethod
    def link(path: Path, name=None) -> str:
        href = path.absolute().as_uri()
        linktext = name if name else path.name
        return '<a href="{}">{}</a>'.format(href, linktext)

    def retrieve_config(self):
        default_conf = self.addonmanager.addonConfigDefaults(self.addonmanager.addonFromModule(__name__))
        conf = self.addonmanager.getConfig(__name__)
        for i in default_conf:
            if i not in conf:
                conf[i] = default_conf[i]
            for j in default_conf[i]:
                if j not in conf[i]:
                    conf[i][j] = default_conf[i][j]
        return conf

    def export_paper(self, deckname: str, cards) -> None:
        self.config = self.retrieve_config()
        htmlfile, pdffile = self.generate_paper(deckname, cards)
        outputdir = htmlfile.parent

        infotext = 'File saved to directory:<br/>\n'
        infotext += 'Dir: ' + self.link(outputdir, outputdir) + '<br/>\n' if outputdir is not None else ''
        pdflink = 'Pdf: ' + self.link(pdffile) + '<br/>\n' if pdffile is not None else ''
        htmllink = 'Html: ' + self.link(htmlfile) + '<br/>\n' if htmlfile is not None else ''

        self.ankiutils.showInfo(infotext + pdflink + htmllink)

    @staticmethod
    def get_instance(ankiutils, addonmanager, mediapath: Path):
        if not Papercard.instance:
            Papercard.instance = Papercard(ankiutils, addonmanager, mediapath)
        return Papercard.instance
