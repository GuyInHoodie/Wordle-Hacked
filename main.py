import pygame
import os
import sys

#A FUNCTION THAT GETS THE WORDS FROM WORDLIST
def get_words():

	with open('WordList.txt','r') as f:

		words = f.read().splitlines()

	return words
words = get_words()
stored_words = words
possible_words = []
green_letters = []


WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hacking Wordle")
pygame.font.init()


FPS = 60
SIZE_OF_SQUARES = 60, 60

#DECLARING SOME VARIABLES
db = {}
KEYS = {97: 'A', 98: 'B', 99: 'C', 100: 'D', 101: 'E', 102: 'F', 103: 'G', 104: 'H', 105: 'I', 106: 'J', 107: 'K', 108: 'L', 109: 'M', 110: 'N', 111: 'O', 112: 'P', 113: 'Q', 114: 'R', 115: 'S', 116: 'T', 117: 'U', 118: 'V', 119: 'W', 120: 'X', 121: 'Y', 122: 'Z'}



BACK_BOX_IMAGE = pygame.image.load(os.path.join("Assets", "Boxes", "Background Textbox.png"))
BACK_BOX = pygame.transform.scale(BACK_BOX_IMAGE, (SIZE_OF_SQUARES))
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont(None,  50)



def get_y_grid(y):
	if 5 <= y <= 65:
		y_coord = 0
	if 70 <= y <= 130:
		y_coord = 1
	if 135 <= y <= 175:
		y_coord = 2
	if 200 <= y <= 260:
		y_coord = 3
	if 265 <= y <= 325:
		y_coord = 4

	return(y_coord)

def get_grid(y, x):
	x_coord = 0
	y_coord = 0

	if 5 <= y <= 65:
		y_coord = 1
	elif 70 <= y <= 130:
		y_coord = 2
	elif 135 <= y <= 175:
		y_coord = 3
	elif 200 <= y <= 260:
		y_coord = 4
	elif 265 <= y <= 325:
		y_coord = 5

	if 5 <= x <= 65:
		x_coord = 1
	elif 70 <= x <= 130:
		x_coord = 2
	elif 135 <= x <= 175:
		x_coord = 3
	elif 200 <= x <= 260:
		x_coord = 4
	elif 265 <= x <= 325:
		x_coord = 5
	elif 330 <= x <= 390:
		x_coord = 6

	if x_coord != 0 and y_coord != 0:
		return x_coord, y_coord
	else:
		pass

def calc_pos(coord):
	position = 5 + (coord - 1) * (60 + 5)
	return position

def is_letter_in_word():
	for d in db:
		letter = db[d][5].lower()
		if db[d][3] == "Gray" and letter not in green_letters:
			for word in words:
				if letter in word:
					possible_words.append(word)
				else:
					pass
		if db[d][3] == "Yellow":
			pos = get_y_grid(db[d][1])

			letter = db[d][5].lower()
			for word in words:
				count = 0
				for i in word:
					if count == pos:
						if not i == letter:
							pass
						else:
							possible_words.append(word)
					count += 1
				if letter in word:
					pass
				else:
					possible_words.append(word)
		if db[d][3] == "Green":
			pos = get_y_grid(db[d][1])
			letter = db[d][5].lower()
			green_letters.append(letter)
			for word in words:
				count = 0
				for i in word:
					if count == pos:
						if i == letter:
							pass
						else:
							possible_words.append(word)
					count += 1
				if letter in word:
					pass
				else:
					possible_words.append(word)

	for i in possible_words:
		try:
			words.remove(i)
		except:
			pass

	print(words)

def store_letter(letter, x_coord, y_coord, colour):
	loaded_letter = pygame.image.load(os.path.join("Assets", "Letters", f"{letter}.png"))
	sized_letter = pygame.transform.scale(loaded_letter, (SIZE_OF_SQUARES))

	loaded_gray_box = pygame.image.load(os.path.join("Assets", "Boxes", "Gray.png"))
	loaded_yellow_box = pygame.image.load(os.path.join("Assets", "Boxes", "Yellow.png"))
	loaded_green_box = pygame.image.load(os.path.join("Assets", "Boxes", "Green.png"))
	sized_gray_box = pygame.transform.scale(loaded_gray_box, (SIZE_OF_SQUARES))
	sized_yellow_box = pygame.transform.scale(loaded_yellow_box, (SIZE_OF_SQUARES))
	sized_green_box = pygame.transform.scale(loaded_green_box, (SIZE_OF_SQUARES))


	db[f"{x_coord} {y_coord}"] = [sized_letter, x_coord, y_coord, colour, {"Gray": sized_gray_box, "Yellow": sized_yellow_box, "Green": sized_green_box}, letter]


def draw_window():
	WIN.fill((0, 0, 0))

	#THIS PART DSIAPLAYS THE BACKGROUND GRAY BOXES
	BACK_BOX_Y = 5
	for column in range(6):
		BACK_BOX_X = 5
		for row in range(5):
			WIN.blit(BACK_BOX, (BACK_BOX_X, BACK_BOX_Y))
			BACK_BOX_X += 65
		BACK_BOX_Y += 65


	#THIS PART DISPLAYS THE LETTERS THAT WAS TYPED
	for i in db:
		WIN.blit(db[i][4][db[i][3]], (db[i][1], db[i][2]))
	for i in db:
		WIN.blit(db[i][0], (db[i][1], db[i][2]))


	#DISPLAYS THE POSSIBLE WORDS
	line = 5
	for w in words[:12]:
		displayed = FONT.render(w, False, WHITE)
		WIN.blit(displayed, (370, line))
		line += 40



	pygame.display.update()


def main():
	
	clock = pygame.time.Clock()
	count = 1
	row_count = 1
	word = ""

	run = True
	while run:
		#SETTING THE TICK SPEED
		clock.tick(FPS)


		#detecting mouse position for buttons
		mouse = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False



			if event.type == pygame.MOUSEBUTTONDOWN:
				try:
					coord = get_grid(mouse[0], mouse[1])
					x, y = coord
					x, y = calc_pos(y), calc_pos(x)
					colour_count = 0

					if db[f"{x} {y}"][3] == "Gray":
						db[f"{x} {y}"][3] = "Yellow"
						colour_count += 1

					if db[f"{x} {y}"][3] == "Yellow" and colour_count == 0:
						db[f"{x} {y}"][3] = "Green"
						colour_count += 1

					if db[f"{x} {y}"][3] == "Green" and colour_count == 0:
						db[f"{x} {y}"][3] = "Gray"
				except:
					pass



			if event.type == pygame.KEYDOWN:
				#THE TRY IS TO MAKE SURE THE GAME DOESN'T CRASH IF YOU TYPE IN SOME OTHER LETTERS
				try:

					if event.key == pygame.K_RETURN:
						if count == 6:
							row_count += 1
							count = 1
							is_letter_in_word()

						else:
							pass


					if event.key == pygame.K_BACKSPACE:
						if count > 1:
							count -= 1
							db.pop(f"{calc_pos(count)} {calc_pos(row_count)}")
						if count == 1 and row_count > 1:
							row_count -= 1
							count = 6
							db.pop(f"{calc_pos(count)} {calc_pos(row_count)}")


					if count < 6 and row_count < 7:
						letter = KEYS[event.key]
						store_letter(KEYS[event.key], calc_pos(count), calc_pos(row_count), "Gray")
						count += 1
				except:
					pass

		draw_window()
	pygame.quit()


if __name__ == "__main__":
	main()