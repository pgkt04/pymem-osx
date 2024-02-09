from typing import List

class Segment:
  def __init__(self, name: str, address: int) -> None:
    self.name: str = name
    self.address: int = address
  def __str__(self) -> str: return self.name
  def __eq__(self, __value: object) -> bool:
    if isinstance(__value, str): return self.name == __value
    elif isinstance(__value, Segment): return self.name == __value.get_name()
    return False
  def get_name(self) -> str: return self.name
  def get_address(self) -> int: return self.address

class Section:
  def __init__(self, name: str, address: int, segments: List[Segment]) -> None:
    self.name: str = name
    self.address: int = address
    self.segments: List[Segment] = segments.copy()
  def __str__(self) -> str: return self.name
  def __eq__(self, __value: object) -> bool:
    if isinstance(__value, str): return self.name == __value
    elif isinstance(__value, Section): return self.name == __value.get_name()
    return False
  def get_name(self) -> str: return self.name
  def get_address(self) -> int: return self.address
  def get_segments(self) -> List[Segment]: return self.segments

class Module:
  def __init__(self, name: str, address: int) -> None:
    self.name: str = name
    self.address: int = address
    self.sections: List[Section] = []
  def __str__(self) -> str: return self.name
  def __eq__(self, __value: object) -> bool:
    if isinstance(__value, str): return self.name == __value
    elif isinstance(__value, Module): return self.name == __value.get_name()
    return False
  def add_sections(self, sections) -> None: self.sections.extend(sections.copy())
  def append_section(self, section) -> None: self.sections.append(section.copy())
  def get_name(self) -> str: return self.name
  def get_address(self) -> int: return self.address
  def get_sections(self) -> List[Section]: return self.sections