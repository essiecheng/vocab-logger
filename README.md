# vocab-logger

A command-line vocabulary logger and quizzer for Chinese learners. Save words you encounter outside of class (e.g. watching TV shows, reading, conversations) and quiz yourself on them later. All stored in one central structured place so you can actually go back and study them.

## Usage

Install the tool:

```
uv add "git+https://github.com/essiecheng/vocab-logger.git"
```

**Add a word/phrase** — pinyin and definition are added by the tool automatically:

```
vocab add "有备而来"
# → Added: 有备而来 — yǒu bèi ér lái — come fully prepared
```

Override the auto-generated fields:

```
vocab add "有备而来" --pinyin "yǒu bèi ér lái" --definition "idiom that translates to 'to come prepared'"
```

Tag a word/phrase with its source in which you discovered it for context:

```
vocab add "有备而来" --tags "对方可是有备而来，我们千万不可掉以轻心"
```

**List words:**

```
# all words
vocab list    
# 10 most recently added              
vocab list --recent 10  
# 10 random words    
vocab list --random 10     
```

**Quiz yourself:**

```
# 10 random questions (shows characters, you type definition)
vocab quiz  
# 20 random questions                
vocab quiz --random 20    
# quiz your 10 most recently added words   
vocab quiz --recent 10 
# show definition, type the characters      
vocab quiz --mode definition  
```

**See your stats:**

```
vocab stats
# → overall accuracy, words quizzed, and your hardest words
```

**Remove a word:**

```
vocab remove "有备而来"
```
