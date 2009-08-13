import rabbyt
import pyglet

#
import random

win = pyglet.window.Window(800, 600)
rabbyt.set_default_attribs()

aliens = [rabbyt.Sprite('alien.png') for i in range(0, 10)]
for i, alien in enumerate(aliens):
	alien.y = win.height-alien.texture.height/2
	alien.x = (alien.texture.width+5)*i+alien.texture.width/2-10


# Create the thing which shoots....
gun = rabbyt.Sprite('gun.png')
gun.y = gun.texture.height/2

# Make the gun move...
from pyglet.window import mouse
@win.event
def on_mouse_motion(x, y, dx, dy):
	gun.x += dx
	# Make sure we can't go outside the window
	gun.x = min(max(0, gun.x), win.width)

pyglet.clock.schedule(rabbyt.add_time)

@pyglet.clock.schedule
def update(dt):
	# Change the direction of the aliens
	if aliens:
		if aliens[0].x-aliens[0].texture.width/2 < 0:
			print "going ---->"
			for i, alien in enumerate(aliens):
				alien.x = rabbyt.lerp(alien.x, win.width+alien.x, dt=5.0)
				alien.y = rabbyt.lerp(alien.y, alien.y-alien.texture.height/2, dt=0.5)

		if aliens[-1].x+aliens[-1].texture.width/2 > win.width:
			print "going <---"
			for i, alien in enumerate(aliens):
				alien.x = rabbyt.lerp(alien.x, -win.width+alien.x, dt=5.0)
				alien.y = rabbyt.lerp(alien.y, alien.y-alien.texture.height/2, dt=0.5)
	else:
		print "You win man!"

	# Check for collisions
	for a, b in rabbyt.collisions.aabb_collide([gun]+bullets_alien):
		if a is gun or b is gun:
			print "Game over man!"
			# Game over man!
			gun.alpha = 0

	for a, b in rabbyt.collisions.aabb_collide(aliens+bullets_my):
		if b in aliens:
			bullets_my.remove(a)
			aliens.remove(b)
		if a in aliens:
			bullets_my.remove(b)
			aliens.remove(a)

	# Clean up any bullets which have left the screen
	for bullets in bullets_my, bullets_alien:
		for bullet in list(bullets):
			if bullet.y > win.height:
				bullets.remove(bullet)
			if bullet.y < 0:
				bullets.remove(bullet)




# Make it possible for me to shoo the aliens
bullets_my = []
@win.event
def on_mouse_press(x, y, b, m):
	if len(bullets_my) < 3:
		bullet = rabbyt.Sprite("bullet.png")
		bullet.x = gun.x
		bullet.y = rabbyt.lerp(gun.y+gun.texture.height/2+bullet.texture.height/2, 
				       win.height+10, dt=2.0)
		bullets_my.append(bullet)

# Make the aliens shoot at me
bullets_alien = []
def shoot(dt):
	if aliens:
		shooter = random.choice(aliens)
		bullet = rabbyt.Sprite("bullet-alien.png")
		bullet.x = shooter.x
		bullet.rot = 180
		bullet.y = rabbyt.lerp(shooter.y-shooter.texture.height/2-bullet.texture.height/2, 
				       -10, dt=2.0)
		bullets_alien.append(bullet)
	
pyglet.clock.schedule_interval(shoot, 1)

# Draw everything..
@win.event
def on_draw():
	rabbyt.clear()
	gun.render()
	rabbyt.render_unsorted(aliens)
	rabbyt.render_unsorted(bullets_my)
	rabbyt.render_unsorted(bullets_alien)
	win.flip()

pyglet.app.run()
