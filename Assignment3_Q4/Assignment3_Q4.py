from bs4 import BeautifulSoup
import re

html = """
<html>
<head>
<title>My first web page</title>
</head>
<body>
<h1>My first web page</h1>
<h2>What this is tutorial</h2>
<p>A simple page put together using HTML. <em>I said a simple page.</em>.</p>
<ul>
<li>To learn HTML</li>
<li>
To show off
<ol>
<li>Grammar (CFG):</li>
<li>To my boss</li>
<li>To my friends</li>
<li>To my cat</li>
<li>To the little talking duck in my brain</li>
</ol>
</li>
<li>Because I have fallen in love with my computer and want to give her some HTML loving.</li>
</ul>
<h3>Where to find the tutorial</h3>
<p><a href="http://www.aaa.com"><img src="http://www.aaa.com/badge1.gif"></a></p>
<h4>Some random table</h4>
<table>
<tr class="tutorial1">
<td>Row 1, cell 1</td>
<td>Row 1, cell 2<img src="http://www.bbb.com/badge2.gif"></td>
<td>Row 1, cell 3</td>
</tr>
<tr class="tutorial2">
<td>Row 2, cell 1</td>
<td>Row 2, cell 2</td>
<td>Row 2, cell 3<img src="http://www.ccc.com/badge3.gif"></td>
</tr>
</table>
</body>
</html>
"""

parser = BeautifulSoup(html, 'html.parser')

#Part a
htmlTitleText = parser.title.string
print(htmlTitleText)

#Part b
liText = parser.find_all('li')[4].text.strip()
print(liText)

#Part c
tdTags = parser.find('tr', class_ = 'tutorial1').find_all('td')
print(tdTags)

#Part d

#Part e
textHTML = parser.find_all(string = re.compile(r'HTML', re.IGNORECASE))
print(textHTML)

#Part f
secondRowText = parser.find('tr', class_ = 'tutorial2').get_text(strip = True)
print(secondRowText)

#Part g
imageTags = parser.find_all('img', attrs = {'src' : True})
print(imageTags)