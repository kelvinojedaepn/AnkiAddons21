# -*- coding: utf-8 -*-

# Remove Clozes Add-on for Anki
#
# Copyright (C) 2016-2019  Aristotelis P. <https//glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the accompanied license file.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License which
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

from anki.hooks import addHook
from aqt import mw

js_cloze_remove = """
function getSelectionHtml() {
    // Based on an SO answer by Tim Down
    var html = "";
    if (typeof window.getSelection != "undefined") {
        var sel = window.getSelection();
        if (sel.rangeCount) {
            var container = document.createElement("div");
            for (var i = 0, len = sel.rangeCount; i < len; ++i) {
                container.appendChild(sel.getRangeAt(i).cloneContents());
            }
            html = container.innerHTML;
        }
    } else if (typeof document.selection != "undefined") {
        if (document.selection.type == "Text") {
            html = document.selection.createRange().htmlText;
        }
    }
    return html;
}
if (typeof window.getSelection != "undefined") {
    // get selected HTML
    var sel = getSelectionHtml();
    sel = sel.replace(/%s/mg, "$2");
    // workaround for duplicate list items:
    var sel = sel.replace(/^(<li>)/, "")
    document.execCommand('insertHTML', false, sel);
    saveField('key');
}
"""

def onRemoveClozesStandalone(editor):
    """Remove cloze markers and hints from selected text"""
    cloze_re = r"\{\{c(\d+)::(.*?)(::(.*?))?\}\}"
    editor.web.eval(js_cloze_remove % cloze_re)


def onSetupEditorButtons21(buttons, editor):
    config = mw.addonManager.getConfig(__name__)
    hotkey = config["hotkey"]
    b = editor.addButton(None, "RemoveClozes", onRemoveClozesStandalone,
                         f"Remove clozes in selected text ({hotkey})",
                         label="RC", keys=hotkey)
    buttons.append(b)
    return buttons


addHook("setupEditorButtons", onSetupEditorButtons21)