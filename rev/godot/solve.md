# rev/godot

> Dear player,
> 
> Vladimir and Estragon converse on various topics while they wait for a man named Godot. While they wait, Pozzo is on his way to the market to sell his slave, Lucky.
> 
> Regards,
> 
> jzt

For this challenge we are given a godot exe and pck file.
Searching online for godot re tool, we can use `https://github.com/GDRETools/gdsdecomp`.

## Part 1: Retrieving the encryption key
Attempting to open the pck gives an error, saying an encryption key is needed. This encryption key is 64 characters long representing 32 bytes.
Since the executable needs to decrypt the pck file, the encryption key must be stored in the executable somewhere. Watching this video `https://www.youtube.com/watch?v=fWjuFmYGoSY` gives us an idea of how to find the encryption key.
The file is so big, it took extremely long to open in ida.
I did this by looking for the string: `'fae.is_null()'`.
This gives us the entire string: `'Condition "fae.is_null()" is true. Returning: false'`
Then we have to look after that to see where the executable writes the encryption key from memory. In the decompilation after that, there is the line:
`v47 = byte_143F78540[v44];`, and it repeats for 32 times.
Likely the encryption key is stored at `byte_143F78540`.
Printing the bytes out we get: `52d066de1115fc479e53fcf821715ad7db73e12df7e557833712136b4ff7529e`.

## Part 2: Decompiling the godot code
Using the encryption key, we can get the source code for the project. After looking at the dialogue files in .godot, there doesn't seem to be anything interesting.

So we want to look at `player.gd`.
```
extends CharacterBody2D

const SPEED = 200.0
const JUMP_VELOCITY = -400.0

@onready var playerSprite = $AnimatedSprite2D
@onready var isAlive = true
@onready var lucky = false
@onready var godot = false
@onready var pozzo = false
@onready var shop = false

func _physics_process(delta: float) -> void:
	if isAlive:
		if Input.is_action_pressed("interact") and is_on_floor():
			if shop:
				if lucky and godot:
					global_position.x = 0
					global_position.y = -10000
				elif godot:
					DialogueManager.show_example_dialogue_balloon(load("res://dialgoue/estragon_godot.dialogue"), "start")
				else:
					DialogueManager.show_example_dialogue_balloon(load("res://dialgoue/estragon.dialogue"), "start")
				
			elif pozzo:
				DialogueManager.show_example_dialogue_balloon(load("res://dialgoue/pozzo.dialogue"), "start")
				lucky = true
		
		if Input.is_action_pressed("jump") and is_on_floor():
			velocity.y = JUMP_VELOCITY
		elif Input.is_action_pressed("move_left"):
			playerSprite.flip_h = true
			velocity.x = -1 * SPEED
			if is_on_floor():
				playerSprite.animation = "move"
		elif Input.is_action_pressed("move_right"):
			playerSprite.flip_h = false
			velocity.x = SPEED
			if is_on_floor():
				playerSprite.animation = "move"
		else:
			velocity.x = 0
			if is_on_floor():
				playerSprite.animation = "idle" 
		
		# Gravity + fall anim
		if not is_on_floor():
			playerSprite.animation = "air"
			velocity += get_gravity() * delta
			
	else:
		playerSprite.animation = "death"
		velocity.x = 0
		
	move_and_slide()
```

In particular, the line `if lucky and godot:` seems suspicious as it moves the player to some weird location.

We can patch that to `if true` to execute once we interact with the shop.

To do this, we can use the command line:
```
gdre_tools.exe --pck-patch=ductf_2025_godot_encrypted.pck --patch-file=player.gd=res://src/player.gd --output=ductf_2025_godot_encrypted_patched.pck --key=52d066de1115fc479e53fcf821715ad7db73e12df7e557833712136b4ff7529e
```

Then rename the new file with the original filename.
After playing the game and interacting with the shop, it leads us to a location with the flag: `DUCTF{THE_BOY_WILL_NEVER_REMEMBER}`
