# GoldenDict2Anki
[中文说明](https://zhuanlan.zhihu.com/p/104513438)  
Automatically save the word that you looked up in GoldenDict to Anki 

When you look up a word in GoldenDict's main window or by a small pop-up window, the word along with its explaination will be saved into Anki simutaneouly.

# Useage:
## requirement
1. Anki & AnkiConnect [link](https://ankiweb.net/shared/info/2055492159)
2. GoldenDict [link](https://sourceforge.net/projects/goldendict/files/early%20access%20builds/)
3. a local dictionary (*.mdx) file

## setting in GoldenDict
1. Open GoldenDict, Click [Edit]--[Dictionaries] --[Source]--[Programs]--[Add], set as following and click [apply]: 
    - Type: HTML
    - Name: set as your wish, Let's call it **Ak** here
    - Command Line: "**YourLocalPah**\GD2Anki.exe" %GDWORD%
    - please be noted that path_to_GD2Anki.exe is double quoted and there is a `space` before %GDWORD%
    - Icon: Any local icon file
    
2. it is suggested to move the  **Ak** dictionary to the last postion, because the saving-to-Anki process takes 3 seconds, not fast enough.
    - Click [Edit]--[Dictionaries] --[Dictionaries], select and drag  **Ak** dictionary to the last and click [OK]
## setting in **Config.ini**   
1. **Make sure you get a deck like below image shows**
   - **DeckName**: the deck you'll save the word into
   - **ModelName**: the model name of the deck
    - **CardFrontName**: the **word** you looked up
    - **CardBackName**: the **explanation** you get from a local dictionary (*.mdx) which is set in **Config.ini**
    -  **Note** : in **Config.ini**, there is no need for double-quotion mark for mdxfile path.  Just like this
```
[Deck]
DeckName=Default
ModelName=Basic
CardFrontName=Front
CardBackName=Back
[Dicts]
mdxfile1 = D:\Downloads\GoldenDict2Anki-master\朗文6中英双解.mdx
mdxfile2 = D:\Downloads\GoldenDict2Anki-master\简明英汉字典增强版.mdx
[Config]
AlertWhenFails=1
```
![image](https://github.com/valuex/GoldenDict2Anki/assets/3627812/45dcd576-a7b0-4cb2-a759-90979225505b)

    
# Based on:
1. mdict_query: [link](https://github.com/mmjang/mdict-query)
