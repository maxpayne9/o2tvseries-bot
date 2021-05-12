import sys, getopt
from o2tvseries import *



class MvDownload(object):
    gen_dict = {}
    s_term = []

    def __init__(self, *args, **kwargs):
        self.s_term.append(sys.argv[1])
        self.argv = sys.argv[2:]
        self.opts,self.args = getopt.getopt(self.argv,'s:e:', ["season=", "episode="])

        print(self.s_term)
        for opt,arg in self.opts:
            if opt in ['-s', 'season']:
                self.s_sn = arg
            elif opt in ['-e', '--episode']:
                self.s_ep = arg
        
        # search params are s_term, s_sn,s_ep
        for term in self.s_term:
            print('...searching for ',term)
            while True:
                self.results = search(term)
                if len(self.results.keys()) > 5:
                    print('Warning!....too many similarities\n...taking the last result\n...if undesirable, CTRL+C and refine your search')
                    break
                break
            for v in list(self.results.keys()):
                if term in str(v.lower()):
                    self.index = list(self.results.keys()).index(v)
                    self.mv_name= list(self.results.keys())[self.index]
                    print("\r...found ",self.mv_name.replace('\n',' '))
            self.link = get_link(self.mv_name, self.results)
            self.tags = link_parser(self.link)
            populate(self.tags, self.gen_dict)
            path_var.append(self.mv_name.split('\n')[0]) # creating paths
            if '*' == self.s_sn: #implying all seasons
                print('...found all {} seasons'.format(len(self.gen_dict.keys())))
               
                for i in list(self.gen_dict.keys()):
                    self.sn_name = i
                    path_var.append(self.sn_name.split('\n')[0]) # creating paths

                    print('...parsing and getting episodes for {}'.format(self.sn_name.split('\n')[0]))
                    self.parse_get(self.sn_name)
                    
            else:    
                for s in list(self.gen_dict.keys()):
                    if 'Season 0{}'.format(self.s_sn) in s: #ensure to check for sn 10 and above
                        print('...found season {}'.format(self.s_sn))
                        self.index = list(self.gen_dict.keys()).index(s)
                        self.sn_name= list(self.gen_dict.keys())[self.index]
                
                        path_var.append(self.sn_name.split('\n')[0]) # creating paths

                self.parse_get(self.sn_name)
               
                    

    def parse_get(self, sn_name):
        '''automating the parsing and getting of the files'''
        
        self.link = get_link(self.sn_name, self.gen_dict)
        self.tags = link_parser(self.link)
        self.gen_dict.clear()
        print('...populating episodes')
        populate(self.tags,self.gen_dict)
        print('...found {} episodes'.format(len(self.gen_dict.keys())))
        get_file(self.gen_dict) 

if __name__ == '__main__':
    try:
        MvDownload()
    except KeyboardInterrupt:
        exit(1)

