import json, os, time,re
from sys import stdout
from configparser import ConfigParser
from pyrogram import Client
from pyrogram.errors import (
	FloodWait,TakeoutInitDelay
)
from pyrogram.types import ChatPrivileges
from os import remove,system,name

def clear_screen():
	system('clear || cls')

def ensure_connection(client_name):

	if client_name == "user":
		useraccount = Client(client_name)
		useraccount.start()
		return useraccount

	if client_name == "bot":
		bot = Client(client_name)
		bot.start()
		return bot

def get_chats(
	client,ORIG,
	DEST,MODE,
	BOT_ID,QUERY
):

	global channel_origem
	global destino
	global chat_ids

	names_ch = []
	ids_ch = []
	list_ch = client.get_dialogs()

	for dialog in list_ch:

		channels_names = str(
			dialog.chat.title or dialog.chat.first_name
		)
		channels_ids = int(dialog.chat.id)
		names_ch.append(channels_names)
		ids_ch.append(channels_ids)

	channel_origem=names_ch.index(ORIG)
	origin_chat = ids_ch[channel_origem]
	chat_ids=get_valid_ids(client,origin_chat,QUERY)

	if DEST=='auto':
		channel_destino = client.create_channel(
			title=f'{names_ch[channel_origem]}-clone'
		)
		destino = channel_destino.id
	else:
		channel_destino=names_ch.index(DEST)
		destino = ids_ch[channel_destino]

	if MODE == "bot":
		chats=[origin_chat,destino]
		for chat in chats:
			client.promote_chat_member(
				chat,BOT_ID,
				ChatPrivileges(can_post_messages=True)
			)
	return origin_chat

def get_config_data(path_file_config):

	config_file = ConfigParser()
	config_file.read(path_file_config)
	default_config = dict(config_file["default"])
	return default_config

def foward_photo(message, destino):

	caption = get_caption(message)
	photo_id = message.photo.file_id
	try:
		tg.send_photo(
			chat_id=destino,
			photo=photo_id,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_photo(message, destino)

def foward_text(message, destino):

	text = message.text
	try:
		tg.send_message(
			chat_id=destino,
			text=text,
			disable_notification=True,
			disable_web_page_preview=True,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_text(message, destino)

def foward_sticker(message, destino):

	sticker_id = message.sticker.file_id
	try:
		tg.send_sticker(chat_id=destino, sticker=sticker_id)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_sticker(message, destino)

def foward_document(message, destino):

	caption = get_caption(message)
	document_id = message.document.file_id
	try:
		tg.send_document(
			chat_id=destino,
			document=document_id,
			disable_notification=True,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_document(message, destino)

def foward_animation(message, destino):

	caption = get_caption(message)
	animation_id = message.animation.file_id
	try:
		tg.send_animation(
			chat_id=destino,
			animation=animation_id,
			disable_notification=True,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_animation(message, destino)

def foward_audio(message, destino):

	caption = get_caption(message)
	audio_id = message.audio.file_id
	try:
		tg.send_audio(
			chat_id=destino,
			audio=audio_id,
			disable_notification=True,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_audio(message, destino)

def foward_voice(message, destino):

	caption = get_caption(message)
	voice_id = message.voice.file_id
	try:
		tg.send_voice(
			chat_id=destino,
			voice=voice_id,
			disable_notification=True,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_voice(message, destino)

def foward_video_note(message, destino):

	video_note_id = message.video_note.file_id
	try:
		tg.send_video_note(
			chat_id=destino,
			video_note=video_note_id,
			disable_notification=True,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_video_note(message, destino)

def foward_video(message, destino):

	caption = get_caption(message)
	video_id = message.video.file_id
	try:
		tg.send_video(
			chat_id=destino,
			video=video_id,
			disable_notification=True,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_video(message, destino)

def foward_poll(message, destino):

	if message.poll.type != "regular":
		return
	try:
		tg.send_poll(
			chat_id=destino,
			question=message.poll.question,
			options=[
				option.text for option in message.poll.options
			],
			is_anonymous=message.poll.is_anonymous,
			allows_multiple_answers=message.poll.allows_multiple_answers,
			disable_notification=True,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_poll(message, destino)

def get_caption(message):

	if message.caption:
		caption = message.caption if premium\
		is True else message.caption[:1024]
	else:
		caption = None
	return caption

def get_sender(message):

	if message.photo:
		return foward_photo
	if message.text:
		return foward_text
	if message.document:
		return foward_document
	if message.sticker:
		return foward_sticker
	if message.animation:
		return foward_animation
	if message.audio:
		return foward_audio
	if message.voice:
		return foward_voice
	if message.video:
		return foward_video
	if message.video_note:
		return foward_video_note
	if message.poll:
		return foward_poll

	print("\nNot recognized message type:\n")
	print(message)
	raise Exception

def get_files_type_excluded_by_input(input_string):

	files_type_excluded = []
	if input_string == "" or "0" in input_string:
		return files_type_excluded
	else:
		if "1" or "photo" not in input_string:
			files_type_excluded += [foward_photo]
		elif "2" or "text" not in input_string:
			files_type_excluded += [foward_text]
		elif "3" or "document" not in input_string:
			files_type_excluded += [foward_document]
		elif "4" or "sticker" not in input_string:
			files_type_excluded += [foward_sticker]
		elif "5" or "animation" not in input_string:
			files_type_excluded += [foward_animation]
		elif "6" or "audio" not in input_string:
			files_type_excluded += [foward_audio]
		elif "7" or "voice" not in input_string:
			files_type_excluded += [foward_voice]
		elif "8" or "video" not in input_string:
			files_type_excluded += [foward_video]
		elif "9" or "poll" not in input_string:
			files_type_excluded += [foward_poll]
		else:
			print("Invalid option! Try again")
			return get_files_type_excluded_by_input(input_string)
	return files_type_excluded

def get_message(origin_chat, message_id):

	try:
		message = tg.get_messages(origin_chat, message_id)
		return message
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	return get_message(origin_chat, message_id)

def get_list_posted(CACHE_FILE,int_task_type):

	if int_task_type == 1:
		if os.path.exists(CACHE_FILE):
			os.remove(CACHE_FILE)
		return []
	else:
		if os.path.exists(CACHE_FILE):
			with open(CACHE_FILE, mode="r") as file:
				posted = json.loads(file.read())
				return posted
		else:
			return []

def wait_a_moment(skip=False):

	if skip:
		time.sleep(SKIP_DELAY_SECONDS)
	else:
		time.sleep(DELAY_AMOUNT)

def update_cache(CACHE_FILE, list_posted):

	with open(CACHE_FILE, mode="w") as file:
		file.write(json.dumps(list_posted))

def get_valid_ids(client,origin_chat,QUERY):

	chat_ids=[]
	print('Getting messages...')

	if QUERY == 'all':
		hist=client.get_chat_history(origin_chat)
		for message in hist:
			if message.media or message.text or message.poll:
				chat_ids.append(message.id)
	else:
		sch=client.search_messages(origin_chat, query=QUERY)
		for message in sch:
			chat_ids.append(message.id)

	chat_ids.sort()
	return chat_ids

def must_be_ignored(func_sender,FILES_TYPE_EXCLUDED) -> bool:

	if func_sender in FILES_TYPE_EXCLUDED:
		wait_a_moment(skip=True)
		return True
	else:
		return False

def ensure_folder_existence(folder_path):

	if not os.path.exists(folder_path):
		os.mkdir(folder_path)

def get_task_file(ORIGIN_CHAT_TITLE, destino):

	ensure_folder_existence("posteds")
	ensure_folder_existence(os.path.join("posteds"))
	if name == 'nt':
		ORIGIN_CHAT_TITLE=re.sub(
			r'[\W_]+', '_',ORIGIN_CHAT_TITLE
		)
	task_file_name = f"{ORIGIN_CHAT_TITLE}-{destino}.json"
	task_file_path = os.path.join("posteds", task_file_name)

	return task_file_path

def progressbar(it, prefix="", size=60, out=stdout):

	count = len(it)
	def show(j):
		x = int(size*j/count)
		print(
			f"{prefix}[{u'#'*x}{('.'*(size-x))}] {j}/{count}",
			end='\r', file=out, flush=True
		)
	show(0)
	for i, item in enumerate(it):
		yield item
		show(i+1)
	print("\n", flush=True, file=out)

def start(
	orig_title,origin_chat_id,NEW,
	LIMIT,TYPE
):

	FILES_TYPE_EXCLUDED = get_files_type_excluded_by_input(TYPE)
	CACHE_FILE = get_task_file(orig_title, destino)

	int_task_type = NEW
	list_posted = get_list_posted(CACHE_FILE,int_task_type)
	ids_to_try=chat_ids[len(list_posted):]
	if LIMIT != 0: ids_to_try=ids_to_try[:LIMIT]
	last=len(ids_to_try)

	for i in progressbar(range(last), "Cloning: ", 40):

		message_id=ids_to_try[i]
		message = get_message(origin_chat_id, message_id)
		func_sender = get_sender(message)

		if must_be_ignored(func_sender,FILES_TYPE_EXCLUDED):
			list_posted += [message.id]
			update_cache(CACHE_FILE, list_posted)
			continue

		func_sender(message, destino)
		list_posted += [message.id]
		update_cache(CACHE_FILE, list_posted)

		if i!=last:
			wait_a_moment()

	print('Task completed!')
	tg.stop()

def ensure_connection(client_name):

	if client_name == "user":
		useraccount = Client(client_name)
		useraccount.start()
		return useraccount

	if client_name == "bot":
		bot = Client(client_name)
		bot.start()
		return bot

def connection(
	client_name:str,
	API_ID:int,
	API_HASH:str,
	BOT_TOKEN
):
	if client_name == "user":
		try:
			useraccount = Client(
				"user", API_ID, API_HASH
			)
			with useraccount:
				useraccount.send_message(
					"me", "Message sent with **Pyrogram**!"
				)
				user_id=useraccount.get_users('me').id
		except Exception as e:
			remove('user.session')
			print(f"Connection failed due to {e}.")
	elif client_name == "bot":
		try:
			bot = Client(
				"bot", API_ID, API_HASH,
				bot_token=BOT_TOKEN
			)
			with bot:
				bot.send_message(
					user_id, "Message sent with **Pyrogram**!"
				)
			BOT_ID=BOT_TOKEN[:BOT_TOKEN.find(':')]
			BOT_ID=f'bot_id:{BOT_ID}'
		except Exception as e:
			remove('bot.session')
			print(f"Connection failed due to {e}.")
	else:
		print('Unrecognized client name.')

	if BOT_TOKEN is not None:
		BOT_ID=BOT_TOKEN[:BOT_TOKEN.find(':')]
		BOT_ID=f'bot_id:{BOT_ID}'
	else: BOT_ID=''

	data=f"[default]\n{BOT_ID}\nuser_delay_seconds:10\n"+\
	"bot_delay_seconds:1.2\nskip_delay_seconds:1"
	with open('config.ini', 'w') as f:
		f.write(data)

def menu():

	global SKIP_DELAY_SECONDS
	global DELAY_AMOUNT
	global tg,premium

	print('\nOptions:\n'+
		'1- Start client\n2- Clone\n3- Exit')
	inp=int(input('\nChoose one: '))

	if inp == 1:

		clear_screen()
		api_id=input('api id: ')
		api_hash=input('api hash: ')
		bot_token=input('bot token (optional): ')

		connection('user',api_id,api_hash,None)
		if bot_token != '':
			connection('bot',api_id,api_hash,bot_token)
		clear_screen()

	elif inp == 2:

		clear_screen()
		orig=input('\nOrigin chat title: ')
		dest=input('Destination chat title (optional): ')
		type=input('Type (optional): ')
		mode=input('Mode (optional): ')
		new=input('New (optional): ')
		query=input('Query (optional): ')
		limit=input('Limit (optional): ')
		clear_screen()

		if dest == '':dest='auto'
		if type == '': type='0'
		if mode == '': mode='user'
		if new == '': new=1
		if query == '':query='all'
		if limit == '': limit=0

		config_data = get_config_data("config.ini")
		USER_DELAY_SECONDS=float(config_data.get("user_delay_seconds"))
		BOT_DELAY_SECONDS=float(config_data.get("bot_delay_seconds"))
		SKIP_DELAY_SECONDS=float(config_data.get("skip_delay_seconds"))
		BOT_ID=config_data.get("bot_id")

		try:
			client=Client('user',takeout=True)
			with client:
				origin_chat=get_chats(
					client,orig,dest,mode,BOT_ID,query
				)
			useraccount = ensure_connection("user")
			premium=useraccount.get_users('me').is_premium
			if mode == "bot":
				bot = ensure_connection("bot")
				tg = bot
				DELAY_AMOUNT = BOT_DELAY_SECONDS
			else:
				tg = useraccount
				DELAY_AMOUNT = USER_DELAY_SECONDS

			clear_screen()
			start(
				orig,origin_chat,int(new),
				int(limit),type
			)
		except TakeoutInitDelay:
			print(
				'Confirm the data export request first.'
			)
			exit()
		except Exception as e:
			print(
				f"It wasn't possible to continue due to {e}\n"
			)
			exit()
	elif inp == 3:
		exit()
	else:
		print('Invalid option. Try again.\n')

if __name__=="__main__":

	clear_screen()
	print(
		'Tip: for optional configurations\n'+
		'you can press enter to use default.'
	)
	while True:
		menu()