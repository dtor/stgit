# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from stgit import argparse
from stgit.commands import common
from stgit.lib import transaction
from stgit.out import out

__copyright__ = """
Copyright (C) 2009, Catalin Marinas <catalin.marinas@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see http://www.gnu.org/licenses/.
"""

help = 'Hide a patch in the series'
kind = 'stack'
usage = ['[options] [--] <patch-range>']
description = """
Hide a range of unapplied patches so that they are no longer shown in
the plain 'series' command output."""

args = [argparse.patch_range(argparse.applied_patches,
                             argparse.unapplied_patches)]
options = [
    argparse.opt('-b', '--branch', args=[argparse.stg_branches],
                 short='Use BRANCH instead of the default branch')]

directory = common.DirectoryHasRepositoryLib()

def func(parser, options, args):
    """Hide a range of patch in the series."""
    stack = directory.repository.current_stack
    trans = transaction.StackTransaction(stack, 'hide')

    if not args:
        parser.error('No patches specified')

    patches = common.parse_patches(args, trans.all_patches)
    for p in patches:
        if p in trans.hidden:
            out.warn('Patch "%s" already hidden' % p)
    patches = [p for p in patches if p not in set(trans.hidden)]

    applied = [p for p in trans.applied if p not in set(patches)]
    unapplied = [p for p in trans.unapplied if p not in set(patches)]
    hidden = patches + trans.hidden

    trans.reorder_patches(applied, unapplied, hidden)
    return trans.run()
