Wordpress Multi-media UPloader (wmup) is a python program that can upload custom wordpress posts with media attachments.

(Actually... now that I think about it, it might only upload media attachments for blubrry powerpress)



### Usage ###
---
When the script is run it looks for your configuration file at ~/etc/wmup/config.json

(that should probably be ~/.config/wmup/config.json)

### Configuration ###
---

example ~/etc/wmup/config.json
```json
{
    "auth": {
        "site": "http://your_wordpress_site.org/xmlrpc.php",
        "user": "YourWordpressUsername",
        "pass": "YourWordpressPassword!42"
    },

    "items": [
        {
            "before": [
                "echo Hello!",
                "echo These work with keys too {path} {@term_1}"
            ],
            "after": "echo you don't need to put a single command in a list",

            "path": "/path/to/media/test.mp3",

            "type": "Your_custom_post_type",
            "publish": false,

            "date": "2014-11-26 10 PM",
            "date-format": "%Y-%m-%d %I %p",
            "zone": -5,

            "content": "{@term_5}",
              
            "@term_1": "These are your",
            "@term_2": "Custom post_type's terms",
            "@term_5": "http://codex.wordpress.org/Taxonomies",
              
            "!comment": "Json values with an exclamation mark in front are ignored",
            "!term_6": "Useful for commenting out a term since json is lacking comments"
        }
    ]
}
```

before and after are lists of commands to run before and after the post is uploaded to wordpress.
You can use these to convert files to the right format and clean up after your're done.

Scripts that you want to run must currently live in ~/etc/wmup/scripts/ 
but they can call anything from there.
