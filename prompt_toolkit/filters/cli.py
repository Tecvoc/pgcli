"""
Filters that accept a `CommandLineInterface` as argument.
"""
from __future__ import unicode_literals
from .base import Filter
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding.vi_state import InputMode as ViInputMode
import six

__all__ = (
    'HasArg',
    'HasCompletions',
    'HasFocus',
    'InFocusStack',
    'HasSearch',
    'HasSelection',
    'HasValidationError',
    'IsAborting',
    'IsDone',
    'IsMultiline',
    'IsReadOnly',
    'IsReturning',
    'RendererHeightIsKnown',
    'InViMode',
    'InEditingMode',
)


class HasFocus(Filter):
    """
    Enable when this buffer has the focus.
    """
    def __init__(self, buffer_name):
        self.buffer_name = buffer_name

    def __call__(self, cli):
        return cli.current_buffer_name == self.buffer_name

    def __repr__(self):
        return 'HasFocus(%r)' % self.buffer_name


class InFocusStack(Filter):
    """
    Enable when this buffer appears on the focus stack.
    """
    def __init__(self, buffer_name):
        self.buffer_name = buffer_name

    def __call__(self, cli):
        return self.buffer_name in cli.buffers.focus_stack

    def __repr__(self):
        return 'InFocusStack(%r)' % self.buffer_name


class HasSelection(Filter):
    """
    Enable when the current buffer has a selection.
    """
    def __call__(self, cli):
        return bool(cli.current_buffer.selection_state)

    def __repr__(self):
        return 'HasSelection()'


class HasCompletions(Filter):
    """
    Enable when the current buffer has completions.
    """
    def __call__(self, cli):
        return cli.current_buffer.complete_state is not None

    def __repr__(self):
        return 'HasCompletions()'


class IsMultiline(Filter):
    """
    Enable in multiline mode.
    """
    def __call__(self, cli):
        return cli.current_buffer.is_multiline()

    def __repr__(self):
        return 'IsMultiline()'


class IsReadOnly(Filter):
    """
    True when the current buffer is read only.
    """
    def __call__(self, cli):
        return cli.current_buffer.read_only()

    def __repr__(self):
        return 'IsReadOnly()'


class HasValidationError(Filter):
    """
    Current buffer has validation error.
    """
    def __call__(self, cli):
        return cli.current_buffer.validation_error is not None

    def __repr__(self):
        return 'HasValidationError()'


class HasArg(Filter):
    """
    Enable when the input processor has an 'arg'.
    """
    def __call__(self, cli):
        return cli.input_processor.arg is not None

    def __repr__(self):
        return 'HasArg()'


class HasSearch(Filter):
    """
    Incremental search is active.
    """
    def __call__(self, cli):
        return cli.is_searching

    def __repr__(self):
        return 'HasSearch()'


class IsReturning(Filter):
    """
    When a return value has been set.
    """
    def __call__(self, cli):
        return cli.is_returning

    def __repr__(self):
        return 'IsReturning()'


class IsAborting(Filter):
    """
    True when aborting. (E.g. Control-C pressed.)
    """
    def __call__(self, cli):
        return cli.is_aborting

    def __repr__(self):
        return 'IsAborting()'


class IsExiting(Filter):
    """
    True when exiting. (E.g. Control-D pressed.)
    """
    def __call__(self, cli):
        return cli.is_exiting

    def __repr__(self):
        return 'IsExiting()'


class IsDone(Filter):
    """
    True when the CLI is returning, aborting or exiting.
    """
    def __call__(self, cli):
        return cli.is_done

    def __repr__(self):
        return 'IsDone()'


class RendererHeightIsKnown(Filter):
    """
    Only True when the renderer knows it's real height.

    (On VT100 terminals, we have to wait for a CPR response, before we can be
    sure of the available height between the cursor position and the bottom of
    the terminal. And usually it's nicer to wait with drawing bottom toolbars
    until we receive the height, in order to avoid flickering -- first drawing
    somewhere in the middle, and then again at the bottom.)
    """
    def __call__(self, cli):
        return cli.renderer.height_is_known

    def __repr__(self):
        return 'RendererHeightIsKnown()'


class InViMode(Filter):
    """
    Check whether we are in a certain Vi mode. (Insert, Replace, Navigation.)
    """
    def __init__(self, mode):
        assert isinstance(mode, six.string_types)
        self.mode = mode

    def __call__(self, cli):
        vi_state = cli.vi_state

        # Always report False when we are waiting for a text object or digraph.
        # (This is the best to avoid inserting key bindings in between the
        # operator and text object.)
        if vi_state.operator_func or vi_state.waiting_for_digraph:
            return False

        # When the current buffer is read-only, always report NAVIGATION mode.
        if cli.current_buffer.read_only():
            input_mode = ViInputMode.NAVIGATION
        else:
            input_mode = vi_state.input_mode

        return input_mode == self.mode

    def __repr__(self):
        return 'InViMode(%r)' % (self.mode, )


class InEditingMode(Filter):
    """
    Check whether a given editing mode is active. (Vi or Emacs.)
    """
    def __init__(self, editing_mode):
        self.editing_mode = editing_mode

    def __call__(self, cli):
        return cli.editing_mode == self.editing_mode

    def __repr__(self):
        return 'InEditingMode(%r)' % (self.editing_mode, )


class CanInsert(Filter):
    """
    When it's possible to insert text.
    (When we are in Emacs mode, or Vi insert mode.)
    """
    def __call__(self, cli):
        return cli.editing_mode != EditingMode.VI or (
                not cli.vi_state.operator_func and
                cli.vi_state.input_mode == ViInputMode.INSERT)

    def __repr__(self):
        return 'CanInsert()'
