from aqt.reviewer import Reviewer

def rev_html(self):
	extra = self.mw.col.conf.get("reviewExtra", "")
	return """
<div id=_mark>&#x2605;</div>
<div id=_flag>&#x2691;</div>
<script> qFade = 0; </script>
<div id=qa></div>
{}
""".format(extra)

Reviewer.revHtml = rev_html
