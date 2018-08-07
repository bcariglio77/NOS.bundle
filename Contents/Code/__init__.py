NAME = 'NOS'
ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME

	HTTP.CacheTime = 300
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
	HTTP.Headers['Cookie'] = 'npo_cc=30'

####################################################################################################
@handler('/video/nos', NAME, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()

	oc.add(DirectoryObject(
		key = Callback(Videos, title="NOS Journaal", url='https://nos.nl/uitzending/nos-journaal'),
		title = "NOS Journaal"
	))
	oc.add(DirectoryObject(
		key = Callback(Videos, title="Nieuwsuur", url='https://nos.nl/uitzending/nieuwsuur'),
		title = "Nieuwsuur"
	))
	oc.add(DirectoryObject(
		key = Callback(Videos, title="NOS Jeugdjournaal", url='https://nos.nl/uitzending/nos-jeugdjournaal'),
		title = "NOS Jeugdjournaal"
	))
	oc.add(DirectoryObject(
		key = Callback(Videos, title="NOS Studio Sport", url='https://nos.nl/uitzending/nos-studio-sport'),
		title = "NOS Studio Sport"
	))
	oc.add(DirectoryObject(
		key = Callback(Videos, title="NOS Studio Sport Eredivisie", url='https://nos.nl/uitzending/nos-studio-sport-eredivisie'),
		title = "NOS Studio Sport Eredivisie"
	))
	oc.add(DirectoryObject(
		key = Callback(Videos, title="NOS Studio Voetbal", url='https://nos.nl/uitzending/nos-studio-voetbal'),
		title = "NOS Studio Voetbal"
	))

	return oc

####################################################################################################
@route('/video/nos/videos', allow_sync=True)
def Videos(title, url):

	oc = ObjectContainer(title2=title)
	html = HTML.ElementFromURL(url)
	sidebar = html.xpath('.//div[@class="broadcast-player__playlist__list"]')[0]

	for video in sidebar.xpath('.//li[@class="broadcast-player__playlist__item"]'):

		video_url = video.xpath('./a/@href')[0]

		if not video_url.startswith('https://'):
			video_url = 'https://nos.nl/%s' % video_url.lstrip('/')

		video_title = video.xpath('.//time//text()')[0].strip()

		oc.add(VideoClipObject(
			url = video_url,
			title = video_title,
			thumb = Resource.ContentsOfURLWithFallback(url='')
		))

	if len(oc) < 1:
		return ObjectContainer(header="Geen video's", message="Deze directory bevat geen video's")

	return oc
