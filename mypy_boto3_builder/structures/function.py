"""
Module-level function.
"""
from collections.abc import Iterable, Iterator
from typing import TypeVar

from mypy_boto3_builder.import_helpers.import_record import ImportRecord
from mypy_boto3_builder.structures.argument import Argument
from mypy_boto3_builder.type_annotations.fake_annotation import FakeAnnotation
from mypy_boto3_builder.type_annotations.type import Type
from mypy_boto3_builder.type_annotations.type_typed_dict import TypeTypedDict

_R = TypeVar("_R", bound="Function")


class Function:
    """
    Module-level function.
    """

    def __init__(
        self,
        name: str,
        arguments: Iterable[Argument],
        return_type: FakeAnnotation,
        docstring: str = "",
        decorators: Iterable[FakeAnnotation] = (),
        body_lines: Iterable[str] = (),
        type_ignore: bool = False,
        is_async: bool = False,
    ):
        self.name = name
        self.arguments = list(arguments)
        self.return_type = return_type
        self.docstring = docstring
        self.decorators = list(decorators)
        self.body_lines = body_lines
        self.type_ignore = type_ignore
        self.request_type_annotation: TypeTypedDict | None = None
        self.is_async = is_async

    def __repr__(self) -> str:
        return (
            f"{'async ' if self.is_async else ''}def"
            f" {self.name}({', '.join(argument.render() for argument in self.arguments)}) ->"
            f" {self.return_type.render()}"
        )

    @property
    def short_docstring(self) -> str:
        """
        Docstring without documentation links.
        """
        if not self.docstring:
            return self.docstring

        short_docstring = self.docstring.strip().split("\n\n")[0]
        if short_docstring.startswith("["):
            return ""
        return short_docstring

    def create_request_type_annotation(self, name: str) -> None:
        """
        Create and set `request_type_annotation` TypedDict based on function arguments.
        """
        result = TypeTypedDict(name)
        for argument in self.arguments:
            if argument.is_kwflag():
                continue

            if not argument.type_annotation:
                continue
            result.add_attribute(
                argument.name,
                argument.type_annotation,
                required=argument.required,
            )

        if not result.children:
            return
        self.request_type_annotation = result

    @property
    def body(self) -> str:
        """
        Function body as a string.
        """
        return "\n".join(self.body_lines)

    def iterate_types(self) -> Iterator[FakeAnnotation]:
        """
        Iterate over required type annotations.
        """
        yield from self.return_type.iterate_types()
        for argument in self.arguments:
            yield from argument.iterate_types()
        for decorator in self.decorators:
            yield from decorator.iterate_types()

    def get_required_import_records(self) -> set[ImportRecord]:
        """
        Extract required import records.
        """
        result: set[ImportRecord] = set()
        for type_annotation in self.iterate_types():
            import_record = type_annotation.get_import_record()
            if not import_record or import_record.is_builtins():
                continue
            result.add(import_record)

        return result

    @property
    def returns_none(self) -> bool:
        """
        Whether return type is None.
        """
        return self.return_type == Type.none

    def is_kw_only(self) -> bool:
        """
        Whether method arguments can be passed only as kwargs.
        """
        return any(arg.is_kwflag() for arg in self.arguments)

    @property
    def type_hint_annotations(self) -> list[FakeAnnotation]:
        """
        Type annotations list from arguments and return type with internal types.
        """
        result: list[FakeAnnotation] = []
        for argument in self.arguments:
            if argument.type_annotation and argument.type_annotation.get_local_types():
                result.append(argument.type_annotation)
        if self.return_type and self.return_type.get_local_types():
            result.append(self.return_type)
        return result

    def copy(self: _R) -> _R:
        """
        Deep copy function.
        """
        return self.__class__(
            name=self.name,
            arguments=[i.copy() for i in self.arguments],
            return_type=self.return_type.copy(),
            docstring=self.docstring,
            decorators=[i.copy() for i in self.decorators],
            body_lines=list(self.body_lines),
            type_ignore=self.type_ignore,
            is_async=self.is_async,
        )

    def remove_argument(self: _R, *names: str) -> _R:
        """
        Remove argument by name.
        """
        remove = [arg for arg in self.arguments if arg.name in names]

        for argument in remove:
            self.arguments.remove(argument)

        return self
