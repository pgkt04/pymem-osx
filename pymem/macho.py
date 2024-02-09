from typing import List

class Segment:
  def __init__(self) -> None: pass

class Section:
  def __init__(self, name: str, address: int, segments: List[Segment]) -> None:
    self.name = name
    self.address = address
    self.segments = segments

class Modules:
  def __init__(self, name, address) -> None:
    self.name = name
    self.address = address
    self.sections = []

  def add_sections(self, sections) -> None: self.sections.extend(sections)
  def add_section(self, section) -> None: self.sections.append(section)
  def get_name(self) -> str: return self.name
  def get_address(self) -> int: return self.address