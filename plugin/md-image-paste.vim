if !has("python3")
  echo "vim has to be compiled with +python3 to run this"
  finish
endif

if exists('g:md_image_paste_loaded')
  finish
endif

let s:save_cpo = &cpo
set cpo&vim

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import plugin
EOF

let g:md_image_paste_loaded = 1

function! PasteImage()
  let with_alttext = input("What is the file name / alt-text? ")
  python3 plugin.paste_image(vim.eval('with_alttext').strip())
endfunction

command! -nargs=0 PasteImage call PasteImage()

let &cpo = s:save_cpo
unlet s:save_cpo
