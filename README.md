# GoldenDict2Anki
Automatically save the word that you looked up in GoldenDict to Anki 

When you look up a word in GoldenDict's main window or by a small pop-up window, the word along with its explaination will be saved into Anki simutaneouly.

# Useage:
## requirement
1. Anki & AnkiConnect [link](https://ankiweb.net/shared/info/2055492159)
2. GoldenDict [link](https://sourceforge.net/projects/goldendict/files/early%20access%20builds/)
3. a local dictionary (*.mdx) file
## setting in Anki
1. Open Anki and install the addon called AnkiConnect to Anki. And ** keep Anki open ** when you want to use this function
2. Add a deck named **NewWords**
## setting in GoldenDict
1. Open GoldenDict, Click [Edit]--[Dictionaries] --[Source]--[Programs]--[Add], set as following and click [apply]: 
    - Type: HTML
    - Name: set as your wish, Let's call it **Ak** here
    - Command Line: "**YourLocalPah**\GD2Anki.exe" %GDWORD%
    - Icon: Any local icon file
    
2. it is suggested to move the  **Ak** dictionary to the last postion, because the saving-to-Anki process takes 3 seconds, not fast enough.
    - Click [Edit]--[Dictionaries] --[Dictionaries], select and drag  **Ak** dictionary to the last and click [OK]
## setting in GD2Anki    
1. **content saved to Anki**
    - Front side: the **word** you looked up
    - Back side: the **explanation** you get from a local dictionary (*.mdx) which is set in **Config.ini**
    
    
# Based on:
1. mdict_query: [link](https://github.com/mmjang/mdict-query)
