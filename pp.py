import os

def walk_blog_folder(blog_folder):
    for root, dirs, files in os.walk(blog_folder):
        for file in files:
            if file.endswith('.html'):
                k = None
                with open(os.path.join(root, file), 'r') as f:
                    k = (f.read()
                     .replace('style.css', '/style.css')
                     .replace('img/', '/img/')
                     .replace('<body>',"""
                              <body>
                              <script src="/root.js"></script>
                              """))
                with open(os.path.join(root, file), 'w') as f:
                    f.write(k)
                    

if __name__ == "__main__":
    blog_folder = 'blog'
    walk_blog_folder(blog_folder)