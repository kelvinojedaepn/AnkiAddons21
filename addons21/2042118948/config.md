### Configuration

#### Section paper
This is for paper and printing settings

<dl>
  <dt>format</dt>
  <dd>Paper format for your region (<b>A4</b> / letter)</dd>

  <dt>orientation</dt>
  <dd>Paper orientation: (<b>landscape</b> / portrait)</dd>
  
  <dt>cardsPerRow</dt>
  <dd>Number of cards which are displayed horizontal (<b>4</b>)</dd>
  
  <dt>cardsPerCol</dt>
  <dd>Number of cards which are displayed vertically (<b>4</b>)</dd>
</dl>

#### Section output
This is for output related settings

<dl>
  <dt>createHtml</dt>
  <dd>html file is created (<b>true</b> / false)</dd>

  <dt>createPdf</dt>
  <dd>pdf file is created (<b>true</b> / false)</dd>

  <dt>path</dt>
  <dd>Directory, where output should be stored. <b>It must exist!</b>:<br/>
    - either constant <b>download</b><br/>
    - or relative path to User Home (MyAnki)<br/>
    - or absolute path (use / instead of \)<br/>
    &nbsp;&nbsp;- Windows: C:/Users/&lt;CurrentUser&gt;/MyAnki<br/>
    &nbsp;&nbsp;- Linux: /home/&lt;CurrentUser&gt;/MyAnki
  </dd>
  
  <dt>filename</dt>
  <dd>first part of the filename: <b>papercard_{deck}</b><br/>
    - variable {deck} might be used for the current exported deck
  </dd>
  
  <dt>filedate</dt>
  <dd>second part of the filename:  (<b>_%y%m%d</b>) in a date formatted form</dd>

  <dt>wkhtmltopdfPath (optional)</dt>
  <dd>Non-standard path to wkhtmltopdf.exe<br/>
    &nbsp;&nbsp;- Windows: C:/Users/&lt;CurrentUser&gt;/wkhtmltox/bin/wkhtmltopdf.exe<br/>
    &nbsp;&nbsp;- Linux: /home/&lt;CurrentUser&gt;/bin/wkhtmltopdf
  </dd>
  
</dl>

#### Section card
This is for card related settings

<dl>
  
  <dt>plaintext</dt>
  <dd>Remove Formatting-Tags of the cards (<b>true</b> / false)</dd>
  
  <dt>repeatQuestionOnAnswer</dt>
  <dd>On answer card the question is also displayed (<b>false</b> / true)</dd>

  <dt>padding</dt>
  <dd>Padding of the card (<b>20</b>). Can be set to 0 to have no space between cards</dd>
  
</dl>