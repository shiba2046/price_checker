
class Queue(object):
    def __init__(self, q = []):
        self.todo = set(q)
        self.done = set()
    
    def add(self, q = []):
        self.todo.update(set(q) - self.done)
    
    def next(self):
        if not self.isdone:
            id = self.todo.pop()
            self.done.add(id)
            return id
        else:
            return None
    
    def dumps(self):
        return '\n'.join(self.done)

    def dump(self, filename='done.txt'):
        with open(filename, 'w') as f:
            f.write(self.dumps())

    @property
    def isdone(self) -> bool:
        return len(self.todo) == 0

    def __repr__(self) -> str:
        return f"Queue: to do: {self.todo} done: {self.done}"


class jd_crawler(object):
    def __init__(self, webdriver):
        self.browser = webdriver
        self.queue= Queue()

    def _find_element_by_selector(self, selector : str) -> str:
        return self.browser.find_element(By.CSS_SELECTOR, selector).text
    
    def _clean_sku_id(self, sku_id: str) -> str:
        return re.search(r'\d{5,}', sku_id).group(0)
        

    def query_sku(self, sku_id: str, add_other_skus = True) -> dict:
        browser = self.browser
        query_selector = lambda selector: browser.find_element(By.CSS_SELECTOR, selector)
        sku_id = self._clean_sku_id(sku_id)
        url = f'https://item.jd.com/{sku_id}.html'
        css_selectors = {
            'sku_type': '[clstag="shangpin|keycount|product|mbNav-3"]',
            'sku_name': 'div.item.selected',
            'price': 'span.p-price',
            'brand': '[clstag="shangpin|keycount|product|pinpai_1"]',
            'shop': '[clstag="shangpin|keycount|product|dianpuname1"',
            'sku_desc': 'div.sku-name',
            'parameter-list': 'ul.parameter2.p-parameter-list'
        }

        result = {
            'sku': sku_id,
            'url': url
        }
        try:
            browser.get(url)
            browser.implicitly_wait(5)
            
    
            result = result | {key: query_selector(value).text for key,value in css_selectors.items()}
            result['price'] = float(result['price'][1:])

            # Property page
            query_selector('li[clstag="shangpin|keycount|product|pcanshutab"]').click()
            property_page = {
                'properties': 'div.Ptable'
            }

            result = result | {key: query_selector(value).text for key,value in property_page.items()}

            # Other SKUs
            if add_other_skus:
                self.queue.add({x.get_dom_attribute('data-sku') for x in browser.find_elements(By.CSS_SELECTOR, 'div[data-sku]')})
                
        except:
            pass
        
        print(result)
        return result
    
    def query_skus(self, sku_ids) -> list:
        
        results = []
        self.queue.add([self._clean_sku_id(x) for x in list(sku_ids)])
        while not self.queue.isdone:
            results.append(self.query_sku(self.queue.next()))

        return results
