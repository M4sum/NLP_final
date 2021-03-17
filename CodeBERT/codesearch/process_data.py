# -*- coding: utf-8 -*-
# Copyright (c) Microsoft Corporation. 
# Licensed under the MIT license.

import gzip
import os
import json
import numpy as np
from more_itertools import chunked

DATA_DIR='/Users/davinci/NU_work/NLP/CodeBERT/data/codesearch/'

def format_str(string):
    for char in ['\r\n', '\r', '\n']:
        string = string.replace(char, ' ')
    return string


def preprocess_test_data(language, test_batch_size=1000):
    path = os.path.join(DATA_DIR, '{}_test_0.jsonl.gz'.format(language))
    print(path)
    with gzip.open(path, 'r') as pf:
        data = pf.readlines()  

    idxs = np.arange(len(data))
    data = np.array(data, dtype=np.object)

    np.random.seed(0)   # set random seed so that random things are reproducible
    np.random.shuffle(idxs)
    data = data[idxs]
    batched_data = chunked(data, test_batch_size)

    print("start processing")
    for batch_idx, batch_data in enumerate(batched_data):
        if len(batch_data) < test_batch_size:
            break # the last batch is smaller than the others, exclude.
        examples = []
        for d_idx, d in enumerate(batch_data): 
            line_a = json.loads(str(d, encoding='utf-8'))
            doc_token = ' '.join(line_a['docstring_tokens'])
            for dd in batch_data:
                line_b = json.loads(str(dd, encoding='utf-8'))
                code_token = ' '.join([format_str(token) for token in line_b['code_tokens']])

                example = (str(1), line_a['url'], line_b['url'], doc_token, code_token)
                example = '<CODESPLIT>'.join(example)
                examples.append(example)

        data_path = os.path.join(DATA_DIR, 'test/{}'.format(language))
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        file_path = os.path.join(data_path, 'batch_{}.txt'.format(batch_idx))
        print(file_path)
        # with open(file_path, 'w', encoding='utf-8') as f:
        #     f.writelines('\n'.join(examples))

def check_parallel_corpus_data(text):
    text = text.replace('DCNL ', "\n").replace("d'", "\ndescription: ").replace("'d ", "\n").replace("DCSP ", "    ").replace("qz", 'd')
    print(text)

if __name__ == '__main__':
    # languages = ['go', 'php', 'python', 'java', 'javascript', 'ruby']
    # languages = ['python']
    # for lang in languages:
    #     preprocess_test_data(lang)
    check_parallel_corpus_data("@frappe.whitelist() DCNL qzef setup_complete(args):d'Calls hooks for `setup_wizarqz_complete`, sets home page as `qzesktop` DCNL anqz clears cache. If wizarqz breaks, calls `setup_wizarqz_exception` hook'd DCSP if cint(frappe.qzb.get_single_value(u'System DCSP Settings', u'setup_complete')): DCNL DCSP  DCSP return DCNL DCSP args = process_args(args) DCNL DCSP try: DCNL DCSP  DCSP if (args.language anqz (args.language != u'english')): DCNL DCSP  DCSP  DCSP set_qzefault_language(get_language_coqze(args.lang)) DCNL DCSP  DCSP frappe.clear_cache() DCNL DCSP  DCSP upqzate_system_settings(args) DCNL DCSP  DCSP upqzate_user_name(args) DCNL DCSP  DCSP for methoqz in frappe.get_hooks(u'setup_wizarqz_complete'): DCNL DCSP  DCSP  DCSP frappe.get_attr(methoqz)(args) DCNL DCSP  DCSP qzisable_future_access() DCNL DCSP  DCSP frappe.qzb.commit() DCNL DCSP  DCSP frappe.clear_cache() DCNL DCSP except: DCNL DCSP  DCSP frappe.qzb.rollback() DCNL DCSP  DCSP if args: DCNL DCSP  DCSP  DCSP traceback = frappe.get_traceback() DCNL DCSP  DCSP  DCSP for hook in frappe.get_hooks(u'setup_wizarqz_exception'): DCNL DCSP  DCSP  DCSP  DCSP frappe.get_attr(hook)(traceback, args) DCNL DCSP  DCSP raise DCNL DCSP else: DCNL DCSP  DCSP for hook in frappe.get_hooks(u'setup_wizarqz_success'): DCNL DCSP  DCSP  DCSP frappe.get_attr(hook)(args)")