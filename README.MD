An attempt at creating a vector embedding similar to the one used for lore except this one can help you with openMW scripting. I included `create-attach-vector-store.py` which can be used to hook it up to your own chatgpt assistant. You can read more about how to use it here: **[LINK](https://github.com/kartoffels123/elderscrolls-lore-bots/tree/master/chatgpt_assistant)**

I recommend hooking it up to gpt-4o-mini with the code interpreter on and (necessary) having the file search hooked up to your Library created with the attach-vector-store code.

## Training Set

1. openMW lua docs: https://openmw.readthedocs.io/en/latest/reference/lua-scripting/index.html
2. openMW code written after Jan 1st 2024 (checking for date and whether requires openmw is in the lua file): https://github.com/MWSE/morrowind-nexus-lua-dump
3. In total 123 jsons with a total mass of ~6.5MB.

## Example:
### Query:
 write a script to say "hello world" when I press X

### Response:
To create a script in OpenMW that displays "Hello, World!" when the "X" key is pressed, you can use the following Lua code:
```lua
-- Save this script as my_lua_mod/scripts/example/player.lua
local ui = require('openmw.ui')

-- Return the script's table
return {
    engineHandlers = {
        onKeyPress = function(key)
            if key.symbol == 'x' then
                ui.showMessage("Hello, World!")
            end
        end
    }
}
```
Instructions to Set Up the Script:
1. Create the Script File: Save the code in a Lua file named player.lua in the directory my_lua_mod/scripts/example/.

2. Register the Script: You need to tell OpenMW to use this script. Create or edit a file called my_lua_mod.omwscripts and include the following line:
```PLAYER:scripts/example/player.lua```
3. Enable the Mod: Make sure that the mod my_lua_mod is enabled in your OpenMW configuration file (openmw.cfg) or through the content manager if using the OpenMW-CS.

How It Works:

The onKeyPress function listens for keyboard events.

When the "X" key is pressed, it checks if the symbol of the pressed key is 'x' and then shows a message box displaying "Hello, World!".

Now every time you press "X" in the game, you will see the message!


## Example 2

### Query:
generate an Image element using the white resource that’s colored purple and occupies the entire screen

### Response:
To create an Image element in OpenMW that occupies the entire screen with a purple color using the white resource, you can use the following Lua code:
```lua
local ui = require('openmw.ui')
local util = require('openmw.util')

-- Create a full screen image with purple color
local function createFullScreenPurpleImage()
    local screenSize = ui.layers[ui.layers.indexOf("HUD")].size

    local purpleImage = ui.create {
        layer = 'HUD',
        type = ui.TYPE.Image,
        props = {
            resource = ui.texture { path = 'white' },
            color = util.color.rgb(128 / 255, 0, 128 / 255), -- RGB for purple
            relativeSize = util.vector2(1, 1), -- full screen
            relativePosition = util.vector2(0, 0), -- position at the top left corner
            size = screenSize, -- set the size to the current screen size
        },
    }

    return purpleImage
end

-- Call the function to create the image
createFullScreenPurpleImage()
```

Explanation:

Image Creation: The script creates an image element using a white texture with a purple color.

Size and Position: It sets the size to cover the full screen by using relativeSize and gets the screen dimensions using ui.layers.

Color: The color is set to purple using RGB values.

How to Use:

1. Incorporate this code into an appropriate Lua script file within your OpenMW mod directory (e.g., `my_lua_mod/scripts/example/fullscreen_purple.lua`).

2. Ensure that the script runs when the mod is loaded. You might need to call this function from an event handler or your main script.

This code will render a purple image that covers the entire screen when executed.

