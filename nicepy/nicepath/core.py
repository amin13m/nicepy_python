# nicepath/core.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import inspect
import shutil
from datetime import datetime
import re
from nicepy.logger import logger
from nicepy.nicepath.exceptios import (
    NicePathError,
    NotADirectoryError,
    NotAFileError,
    PathNotFoundError,
    WriteError,
    DeleteError
)

@dataclass
class NicePath:
    """
    📝 NicePath: A powerful, user-friendly wrapper around pathlib.Path with logging, smart search, and tree view.

    Hint (English):
        - _input_path: str or Path - input path for initialization
        - base_dir: Optional base path for relative paths

    راهنمای فارسی:
        - _input_path: مسیر فایل/پوشه ورودی (str یا Path)
        - base_dir: مسیر پایه برای مسیرهای نسبی
    """
    _input_path: str | Path
    base_dir: Path | None = None

    def __post_init__(self):
        """Initialize internal resolved path"""
        if isinstance(self._input_path, Path):
            self._path: Path = self._input_path.resolve()
            return

        input_path = Path(self._input_path)
        if input_path.is_absolute():
            self._path = input_path.resolve()
            return

        # relative path based on caller file
        caller_file = inspect.stack()[1].filename
        base = Path(caller_file).resolve().parent if self.base_dir is None else Path(self.base_dir).resolve()
        self._path: Path = (base / input_path).resolve()

    # -------------------------
    # Logger helpers
    # -------------------------
    def _log_start(self, action: str):
        logger.debug(f"{action} started -> {self._path}")

    def _log_success(self, action: str):
        logger.info(f"{action} success -> {self._path}")

    def _log_error(self, action: str, e: Exception):
        logger.exception(f"{action} failed -> {self._path} | Reason: {e}")

    # -------------------------
    # Info Properties
    # -------------------------
    @property
    def path(self) -> Path:
        """Return the internal resolved Path object / برگرداندن مسیر"""
        return self._path

    @property
    def name(self) -> str:
        """File or folder name (with extension) / نام فایل یا پوشه"""
        return self._path.name

    @property
    def stem(self) -> str:
        """File name without extension / نام فایل بدون پسوند"""
        return self._path.stem

    @property
    def suffix(self) -> str:
        """File extension / پسوند فایل"""
        return self._path.suffix

    @property
    def parent(self) -> NicePath:
        """Return parent folder as NicePath / پوشه والد به صورت NicePath"""
        return NicePath(self._path.parent)

    @property
    def exists(self) -> bool:
        """Check if path exists / بررسی وجود مسیر"""
        return self._path.exists()

    @property
    def is_file(self) -> bool:
        """Check if path is a file / بررسی اینکه مسیر فایل است"""
        return self._path.is_file()

    @property
    def is_dir(self) -> bool:
        """Check if path is a directory / بررسی اینکه مسیر پوشه است"""
        return self._path.is_dir()

    @property
    def size(self) -> int:
        """Return file size or total folder size in bytes / حجم فایل یا کل پوشه"""
        if self.is_file:
            return self._path.stat().st_size
        return sum(p.stat().st_size for p in self._path.rglob("*") if p.is_file())

    @property
    def created_at(self) -> datetime:
        """Return creation datetime / زمان ایجاد فایل یا پوشه"""
        return datetime.fromtimestamp(self._path.stat().st_ctime)

    @property
    def modified_at(self) -> datetime:
        """Return last modification datetime / زمان آخرین ویرایش"""
        return datetime.fromtimestamp(self._path.stat().st_mtime)
        # -------------------------
    # File Actions
    # -------------------------
    def read(self, encoding: str = "utf-8") -> str:
        """
        Read file content / خواندن محتوای فایل

        Args:
            encoding: File encoding / انکودینگ فایل

        Returns:
            str: file content / محتوای فایل
        """
        self._log_start("read")
        if not self.exists:
            self._log_error("read", PathNotFoundError(f"{self._path} not found"))
            raise PathNotFoundError(f"File not found: {self._path}")

        if not self.is_file:
            self._log_error("read", NotAFileError(f"{self._path} is not a file"))
            raise NotAFileError(f"Cannot read because it is not a file: {self._path}")

        try:
            content = self._path.read_text(encoding=encoding)
            self._log_success("read")
            return content
        except Exception as e:
            self._log_error("read", e)
            raise

    def write(self, data: str, encoding: str = "utf-8") -> NicePath:
        """
        Write text to file / نوشتن متن در فایل

        Returns:
            self / خود شیء برای زنجیره متدها
        """
        self._log_start("write")
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(data, encoding=encoding)
            self._log_success("write")
            return self
        except Exception as e:
            self._log_error("write", e)
            raise WriteError(f"Failed to write file: {self._path}") from e

    def append(self, data: str, encoding: str = "utf-8") -> NicePath:
        """
        Append text to file / اضافه کردن متن به فایل
        """
        self._log_start("append")
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("a", encoding=encoding) as f:
                f.write(data)
            self._log_success("append")
            return self
        except Exception as e:
            self._log_error("append", e)
            raise WriteError(f"Failed to append file: {self._path}") from e

    def mkdir(self, parents: bool = True, exist_ok: bool = True) -> NicePath:
        """
        Create directory / ایجاد پوشه
        """
        self._log_start("mkdir")
        try:
            self._path.mkdir(parents=parents, exist_ok=exist_ok)
            self._log_success("mkdir")
            return self
        except Exception as e:
            self._log_error("mkdir", e)
            raise NicePathError(f"Failed to create directory: {self._path}") from e

    def delete(self) -> NicePath:
        """
        Delete file or directory / حذف فایل یا پوشه
        """
        self._log_start("delete")
        if not self.exists:
            self._log_error("delete", PathNotFoundError(f"{self._path} not found"))
            raise PathNotFoundError(f"Path not found: {self._path}")

        try:
            if self.is_file:
                self._path.unlink()
            elif self.is_dir:
                shutil.rmtree(self._path)
            self._log_success("delete")
            return self
        except Exception as e:
            self._log_error("delete", e)
            raise DeleteError(f"Failed to delete: {self._path}") from e

    def copy_to(self, destination: NicePath) -> NicePath:
        """
        Copy file or folder to destination / کپی فایل یا پوشه
        """
        self._log_start("copy_to")
        try:
            dest = Path(destination._path)
            if self.is_file:
                shutil.copy2(self._path, dest)
            else:
                shutil.copytree(self._path, dest, dirs_exist_ok=True)
            self._log_success("copy_to")
            return NicePath(dest)
        except Exception as e:
            self._log_error("copy_to", e)
            raise NicePathError(f"Failed to copy to {destination._path}") from e

    def move_to(self, destination: NicePath) -> NicePath:
        """
        Move file or folder to destination / انتقال فایل یا پوشه
        """
        self._log_start("move_to")
        try:
            dest = shutil.move(self._path, destination._path)
            self._log_success("move_to")
            return NicePath(dest)
        except Exception as e:
            self._log_error("move_to", e)
            raise NicePathError(f"Failed to move to {destination._path}") from e

    # -------------------------
    # Tree View
    # -------------------------
    def tree(
        self,
        recursive: bool = True,
        ignore_hidden: bool = True,
        ignore_venv: bool = True,
    ) -> str:
        """
        EN:
        Generate a visual tree representation of the directory structure.

        FA:
        تولید نمایش گرافیکی درختی از ساختار فایل‌ها و پوشه‌ها.

        Parameters
        ----------
        recursive : bool, default=True
            EN: If True, traverses subdirectories recursively.
            FA: اگر True باشد، زیرپوشه‌ها را نیز به صورت بازگشتی بررسی می‌کند.

        ignore_hidden : bool, default=True
            EN: If True, hidden files and folders (starting with ".") are ignored.
            FA: اگر True باشد، فایل‌ها و پوشه‌های مخفی نادیده گرفته می‌شوند.

        ignore_venv : bool, default=True
            EN: If True, any folder named 'venv' and its entire subtree will be skipped.
            FA: اگر True باشد، پوشه venv و تمام زیرمجموعه آن نادیده گرفته می‌شود.

        Returns
        -------
        str
            EN: A formatted tree string.
            FA: رشته‌ای شامل ساختار درختی مسیر.

        Notes
        -----
        EN:
            - Safe by default (venv ignored)
            - Does not raise error if path does not exist (returns empty string)

        FA:
            - به صورت پیش‌فرض ایمن است (venv نادیده گرفته می‌شود)
            - اگر مسیر وجود نداشته باشد خطا نمی‌دهد و رشته خالی برمی‌گرداند
        """

        self._log_start("tree")

        if not self.exists:
            logger.warning(f"Tree skipped (path not found) -> {self._path}")
            return ""

        try:
            lines: list[str] = []

            def build_tree(path: Path, prefix=""):
                entries = list(path.iterdir())

                # ---- Filters ----
                filtered: list[Path] = []
                for e in entries:
                    if ignore_hidden and e.name.startswith("."):
                        continue
                    if ignore_venv and e.is_dir() and e.name.lower() == "venv":
                        logger.debug(f"tree skipped venv -> {e}")
                        continue
                    filtered.append(e)

                filtered.sort(key=lambda x: (x.is_file(), x.name.lower()))

                for index, entry in enumerate(filtered):
                    connector = "└── " if index == len(filtered) - 1 else "├── "
                    lines.append(prefix + connector + entry.name)

                    if entry.is_dir() and recursive:
                        extension = "    " if index == len(filtered) - 1 else "│   "
                        build_tree(entry, prefix + extension)

            lines.append(self._path.name)

            if self.is_dir:
                build_tree(self._path)

            self._log_success("tree")
            return "\n".join(lines)

        except Exception as e:
            self._log_error("tree", e)
            return ""
        
    # -------------------------
    # Smart Search
    # -------------------------

    def search(
        self,
        name_contains: str | None = None,
        suffix: str | None = None,
        stem: str | None = None,
        regex: str | None = None,
        min_size: int | None = None,
        max_size: int | None = None,
        only_files: bool = False,
        only_dirs: bool = False,
        recursive: bool = True,
        ignore_hidden: bool = True,
        ignore_venv: bool = True,
    ) -> list["NicePath"]:
        """
        EN:
        Advanced file and directory search with multiple filters.
    
        FA:
        جستجوی پیشرفته فایل و پوشه با فیلترهای متنوع.
    
        Parameters
        ----------
        name_contains : str | None
            EN: Return items whose name contains this substring (case-insensitive).
            FA: فایل‌هایی که نام آن‌ها شامل این رشته باشد.
    
        suffix : str | None
            EN: Filter by file extension (e.g. ".py").
            FA: فیلتر بر اساس پسوند فایل (مثلاً ".py").
    
        stem : str | None
            EN: Match exact file name without extension.
            FA: تطابق دقیق نام فایل بدون پسوند.
    
        regex : str | None
            EN: Apply regex pattern to file name.
            FA: اعمال عبارت منظم روی نام فایل.
    
        min_size : int | None
            EN: Minimum file size in bytes.
            FA: حداقل اندازه فایل (بر حسب بایت).
    
        max_size : int | None
            EN: Maximum file size in bytes.
            FA: حداکثر اندازه فایل (بر حسب بایت).
    
        only_files : bool, default=False
            EN: Return only files.
            FA: فقط فایل‌ها را برگرداند.
    
        only_dirs : bool, default=False
            EN: Return only directories.
            FA: فقط پوشه‌ها را برگرداند.
    
        recursive : bool, default=True
            EN: Search recursively in subdirectories.
            FA: جستجوی بازگشتی در زیرپوشه‌ها.
    
        ignore_hidden : bool, default=True
            EN: Ignore hidden files and folders.
            FA: نادیده گرفتن فایل‌ها و پوشه‌های مخفی.
    
        ignore_venv : bool, default=True
            EN: Ignore any folder named 'venv' and its subtree.
            FA: نادیده گرفتن پوشه venv و تمام زیرمجموعه آن.
    
        Returns
        -------
        list[NicePath]
            EN: A list of NicePath objects matching filters.
            FA: لیستی از اشیاء NicePath مطابق با فیلترها.
    
        Safety
        ------
        EN:
            - venv is ignored by default for safety and performance.
            - Returns empty list if nothing is found (no exception).
    
        FA:
            - به صورت پیش‌فرض venv نادیده گرفته می‌شود.
            - در صورت عدم یافتن نتیجه، آرایه خالی برمی‌گرداند و خطا نمی‌دهد.
        """
    
        self._log_start("search")
    
        if not self.exists:
            logger.warning(f"Search skipped (path not found) -> {self._path}")
            return []
    
        candidates = (
            [self._path]
            if self.is_file
            else (self._path.rglob("*") if recursive else self._path.glob("*"))
        )
    
        results: list[NicePath] = []
    
        for p in candidates:
        
            # ---- Skip hidden ----
            if ignore_hidden and p.name.startswith("."):
                continue
            
            # ---- Skip venv folders and their children ----
            if ignore_venv and any(part.lower() == "venv" for part in p.parts):
                logger.debug(f"search skipped venv path -> {p}")
                continue
            
            if only_files and not p.is_file():
                continue
            
            if only_dirs and not p.is_dir():
                continue
            
            if name_contains and name_contains.lower() not in p.name.lower():
                continue
            
            if suffix and p.suffix.lower() != suffix.lower():
                continue
            
            if stem and stem.lower() != p.stem.lower():
                continue
            
            if regex:
                try:
                    if not re.search(regex, p.name):
                        continue
                except re.error as e:
                    self._log_error("search-regex", e)
                    continue
                
            if p.is_file():
                size = p.stat().st_size
                if min_size is not None and size < min_size:
                    continue
                if max_size is not None and size > max_size:
                    continue
                
            results.append(NicePath(p))
    
        self._log_success("search")
        return results
    
    # -------------------------
    # logAll: Tree + Search + Save to file
    # -------------------------

    def logAll(
        self,
        file_output: "NicePath",
        search_name_contains: str | None = None,
        search_suffix: str | None = None,
        search_stem: str | None = None,
        search_regex: str | None = None,
        search_only_files: bool = True,
        search_only_dirs: bool = False,
        search_recursive: bool = True,
        search_ignore_hidden: bool = True,
        max_files: int = 500,          # safety: max number of files to log
        max_total_size: int = 50_000_000,  # safety: max total bytes (50MB)
        ignore_venv: bool = True,      # ignore virtual environments by default
        ignore_libs: bool = True,      # ignore internal library folders by default
        encoding: str = "utf-8"
    ) -> str:
        """
        Log full structure: Tree + search results into a file

        EN:
        Logs the tree of the current path and all matching search files line by line.
        - Safety limits prevent logging too many files or too large total size.
        - Automatically skips venv and library folders by default.
        - If the original path does not exist, logs until last existing parent with a warning.

        FA:
        ساختار درختی مسیر و تمام فایل‌های مطابق با سرچ را خط به خط لاگ می‌کند.
        - محدودیت‌های ایمنی از لاگ بیش از حد فایل‌ها یا حجم جلوگیری می‌کند.
        - به صورت پیشفرض پوشه‌های venv و کتابخانه‌ها را ایگنور می‌کند.
        - در صورت وجود نداشتن مسیر اصلی، تا آخرین مسیر موجود لاگ می‌کند و هشدار می‌دهد.

        Returns:
            str: full text (tree + files) for printing or saving

        ------------------------------------------------------------
    
        Parameters
        ----------
        file_output : NicePath
            EN: Destination file to store the generated log.
            FA: فایل مقصد برای ذخیره گزارش.
    
        search_name_contains : str | None
            EN: Filter by substring in filename.
            FA: فیلتر بر اساس بخشی از نام فایل.
    
        search_suffix : str | None
            EN: Filter by file extension (e.g. ".py").
            FA: فیلتر بر اساس پسوند فایل.
    
        search_stem : str | None
            EN: Match exact filename without extension.
            FA: تطابق دقیق نام فایل بدون پسوند.
    
        search_regex : str | None
            EN: Apply regex pattern to filename.
            FA: اعمال عبارت منظم روی نام فایل.
    
        search_only_files : bool, default=True
            EN: Include only files in search results.
            FA: فقط فایل‌ها در نتایج جستجو لحاظ شوند.
    
        search_only_dirs : bool, default=False
            EN: Include only directories in search results.
            FA: فقط پوشه‌ها در نتایج لحاظ شوند.
    
        search_recursive : bool, default=True
            EN: Search subdirectories recursively.
            FA: جستجوی بازگشتی در زیرپوشه‌ها.
    
        search_ignore_hidden : bool, default=True
            EN: Ignore hidden files and folders.
            FA: نادیده گرفتن فایل‌ها و پوشه‌های مخفی.
    
        safe_mode : bool, default=True
            EN:
                Enables protection limits:
                    - max_files
                    - max_file_size
                    - ignore_venv
            FA:
                فعال‌سازی محدودیت‌های ایمنی شامل:
                    - حداکثر تعداد فایل
                    - حداکثر حجم فایل
                    - نادیده گرفتن venv
    
        max_files : int, default=200
            EN: Maximum number of files to log.
            FA: حداکثر تعداد فایل قابل ثبت در گزارش.
    
        max_file_size : int, default=1_000_000 (1MB)
            EN: Maximum file size allowed for reading (in bytes).
            FA: حداکثر حجم فایل برای خواندن (بر حسب بایت).
    
        ignore_venv : bool, default=True
            EN: Ignore 'venv' directories and their subtree.
            FA: نادیده گرفتن پوشه venv و زیرمجموعه آن.
    
        encoding : str, default="utf-8"
            EN: Encoding used when writing output file.
            FA: نوع انکودینگ برای نوشتن فایل خروجی.
    
        ------------------------------------------------------------
        
        Warning
        -------
        EN:
            Disabling safe_mode on very large projects may cause
            high memory usage and long execution time.
    
        FA:
            خاموش کردن safe_mode در پروژه‌های بسیار بزرگ
            ممکن است باعث مصرف بالای حافظه و کندی سیستم شود.
        
        """
        self._log_start("logAll")

        try:
            lines: list[str] = []

            # ---------- Safety: find last existing parent ----------
            path_to_use = self._path
            while not path_to_use.exists() and path_to_use.parent != path_to_use:
                path_to_use = path_to_use.parent

            if path_to_use != self._path:
                logger.warning(
                    f"logAll: Path {self._path} not found, logging stopped at {path_to_use}"
                )

            # ---------- Tree ----------
            tree_text = NicePath(path_to_use).tree(
                recursive=True, ignore_hidden=not search_ignore_hidden
            )
            lines.append("Tree Structure:\n")
            lines.append(tree_text + "\n\n")

            # ---------- Search ----------
            search_results = NicePath(path_to_use).search(
                name_contains=search_name_contains,
                suffix=search_suffix,
                stem=search_stem,
                regex=search_regex,
                only_files=search_only_files,
                only_dirs=search_only_dirs,
                recursive=search_recursive,
                ignore_hidden=search_ignore_hidden,
            )

            # Apply safety filters
            total_size = 0
            logged_files = 0
            output_lines: list[str] = []

            for f in search_results:
                if ignore_venv and "venv" in f.path.parts:
                    continue
                if ignore_libs and "nicepy" in f.path.parts:
                    continue

                try:
                    content = f.read()
                except Exception as e:
                    content = f"[Could not read: {e}]"

                file_size = len(content.encode(encoding))
                total_size += file_size
                logged_files += 1

                if logged_files > max_files:
                    output_lines.append(
                        f"[Safety Limit] Skipped remaining files, max_files={max_files}\n"
                    )
                    break
                if total_size > max_total_size:
                    output_lines.append(
                        f"[Safety Limit] Max total_size reached, {max_total_size} bytes\n"
                    )
                    break

                output_lines.append(f"{f.path} -> {content}\n")

            if output_lines:
                lines.append("Search Results:\n")
                lines.extend(output_lines)
            else:
                lines.append("Search Results: None\n")

            # ---------- Write to file ----------
            file_output.write("".join(lines), encoding=encoding)

            self._log_success("logAll")
            return "".join(lines)
        except Exception as e:
            self._log_error("logAll", e)
            raise NicePathError(f"logAll failed for {self._path}") from e
    
    # -------------------------
    # Operator Overloads
    # -------------------------

    def __truediv__(self, other: str) -> "NicePath":
        """
        Path division operator / استفاده از / برای ساخت مسیر جدید
        """
        return NicePath(self._path / other)

    def __str__(self) -> str:
        return str(self._path)

    def __repr__(self) -> str:
        return f"NicePath({self._path})"