/* 
Remove Clozes Add-on for Anki

Copyright (C) 2016-2022  Aristotelis P. <https//glutanimate.com/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version, with the additions
listed at the end of the accompanied license file.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

NOTE: This program is subject to certain additional terms pursuant to
Section 7 of the GNU Affero General Public License.  You should have
received a copy of these additional terms immediately following the
terms and conditions of the GNU Affero General Public License which
accompanied this program.

If not, please request a copy through one of the means of contact
listed here: <https://glutanimate.com/contact/>.

Any modifications to this file must keep this entire header intact.
*/

const getSelectedHTML = () => {
  if (!document.activeElement) {
    return null;
  }
  const fieldShadowRoot = document.activeElement.shadowRoot;
  if (!fieldShadowRoot) {
    return null;
  }

  let html;
  const selection = fieldShadowRoot.getSelection();
  if (selection.rangeCount) {
    const container = document.createElement("div");
    for (let i = 0, len = selection.rangeCount; i < len; ++i) {
      container.appendChild(selection.getRangeAt(i).cloneContents());
    }
    html = container.innerHTML;
  }
  return html;
};

function removeClozes() {
  let selectedHTML = getSelectedHTML();
  if (!selectedHTML) {
    return;
  }
  selectedHTML = selectedHTML.replace(
    /\{\{c(\d+)::(.*?)(::(.*?))?\}\}/gm,
    "$2"
  );
  // workaround for duplicate list items:
  selectedHTML = selectedHTML.replace(/^(<li>)/, "");
  document.execCommand("insertHTML", false, selectedHTML);
  globalThis.saveNow();
}
