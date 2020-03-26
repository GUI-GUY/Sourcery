from os import getcwd, path, listdir
from PIL import Image

class DIllustration():
    """Includes all meta information on the downloaded image such as names, locations..."""
    def __init__(self, input_path, illustration_list, minsim):
        self.input_path = input_path # Path to the image in the input folder
        self.original_sub = SubDIllustration(illustration_list[0]['service'], (None, illustration_list[0]['name'], {"path":illustration_list[0]['work_path'], "source":[], "similarity":0}), minsim)
        self.pixiv_subdillustration = list()
        for elem in illustration_list[1]:
            ill = SubDIllustration('Pixiv', elem, minsim)
            if ill.validity_check():
                self.pixiv_subdillustration.append(ill)
        self.danbooru_subdillustration = list()
        for elem in illustration_list[2]:
            ill = SubDIllustration('Danbooru', elem, minsim)
            if ill.validity_check():
                self.danbooru_subdillustration.append(ill)
        self.yandere_subdillustration = list()
        for elem in illustration_list[3]:
            ill = SubDIllustration('Yandere', elem, minsim)
            if ill.validity_check():
                self.yandere_subdillustration.append(ill)
        self.konachan_subdillustration = list()
        for elem in illustration_list[4]:
            ill = SubDIllustration('Konachan', elem, minsim)
            if ill.validity_check():
                self.konachan_subdillustration.append(ill)

class SubDIllustration():
    """Includes all meta information on the downloaded image such as names, locations..."""
    def __init__(self, service, data_triple, minsim):
        self.service = service
        self.id = None
        self.name = data_triple[1]
        dot = self.name.rfind('.')
        if dot == -1:
            self.name_no_suffix = self.name
            self.filetype = ''
        else:
            self.name_no_suffix = self.name[:dot]
            self.filetype = self.name[dot+1:]
        self.path = getcwd() + '/Sourcery/sourced_progress/' + service.lower() + '/' + self.name
        self.title = None
        self.caption = None
        self.description = None
        self.create_date = None
        self.creator = None
        self.width = None
        self.height = None
        if type(data_triple[2]['source']) == type(list()):
            self.source = data_triple[2]['source']
        else:
            self.source = [data_triple[2]['source']]
        self.similarity = float(data_triple[2]['similarity'])
        self.minsim = minsim
        self.is_folder = path.isdir(self.path)
        self.tags = list()

        if service == 'Pixiv':
            self.pixiv_init(data_triple)
        elif service == 'Danbooru':
            self.danbooru_init(data_triple)
        elif service == 'Yandere':
            self.yandere_init(data_triple)
        elif service == 'Konachan':
            self.konachan_init(data_triple)
        elif service == 'Original':
            self.path = data_triple[2]['path']


    def pixiv_init(self, data_triple):
        illustration = data_triple[0]
        self.id = illustration.id
        self.tags = illustration.tags
        self.title = illustration.title
        self.caption = illustration.caption
        self.description = illustration.description
        self.create_date = illustration.create_date
        self.width = str(illustration.width)
        self.height = str(illustration.height)
        self.creator = illustration.user.name
    
    def danbooru_init(self, data_triple):
        illustration = data_triple[0]
        self.id = illustration['id']
        self.title = 'N/A'
        self.caption = 'N/A'
        self.description = 'N/A'
        self.create_date = illustration['created_at']
        self.width = str(illustration['image_width'])
        self.height = str(illustration['image_height'])
        self.creator = illustration['tag_string_artist']
        for tag in illustration['tag_string_general'].strip("'").split():
            self.tags.append(tag)
        for tag in illustration['tag_string_character'].strip("'").split():
            self.tags.append('character:' + tag)
        for tag in illustration['tag_string_copyright'].strip("'").split():
            self.tags.append('copyright:' + tag)
        for tag in illustration['tag_string_artist'].strip("'").split():
            self.tags.append('creator:' + tag)
        for tag in illustration['tag_string_meta'].strip("'").split():
            self.tags.append('meta:' + tag)
        self.tags.append('source:' + illustration['source'])
        self.tags.append('rating:' + illustration['rating'])
        self.tags.append('booru:danbooru')
        if illustration['pixiv_id'] != None:
            self.tags.append('pixiv work:' + str(illustration['pixiv_id']))

    def yandere_init(self, data_triple):
        illustration = data_triple[0]
        self.id = illustration['id']
        self.title = 'N/A'
        self.caption = 'N/A'
        self.description = 'N/A'
        self.create_date = illustration['created_at']
        self.width = str(illustration['width'])
        self.height = str(illustration['height'])
        self.creator = 'N/A'
        for tag in illustration['tags'].strip("'").split():
            self.tags.append(tag)
        self.tags.append('rating:' + illustration['rating'])
        self.tags.append('booru:yande.re')
    
    def konachan_init(self, data_triple):
        illustration = data_triple[0]
        self.id = illustration['id']
        self.title = 'N/A'
        self.caption = 'N/A'
        self.description = 'N/A'
        self.create_date = illustration['created_at']
        self.width = str(illustration['width'])
        self.height = str(illustration['height'])
        self.creator = 'N/A'
        for tag in illustration['tags'].strip("'").split():
            self.tags.append(tag)
        self.tags.append('rating:' + illustration['rating'])
        self.tags.append('booru:konachan')

    def validity_check(self):
        if not self.name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            return False 
        if self.is_folder:
            if len(listdir(self.path)) <= 0:
                return False
        elif path.isfile(self.path):
            if not self.path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                return False
        else:
            return False
        return True