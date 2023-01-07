---

database-plugin: basic

---

```yaml:dbfolder
name: new database
description: new description
columns:
  __file__:
    key: __file__
    id: __file__
    input: markdown
    label: File
    accessorKey: __file__
    isMetadata: true
    skipPersist: false
    isDragDisabled: false
    csvCandidate: true
    position: 1
    isHidden: false
    sortIndex: -1
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: true
      task_hide_completed: true
      footer_type: none
  birthday:
    input: calendar
    accessorKey: birthday
    key: birthday
    id: birthday
    label: birthday
    position: 100
    skipPersist: false
    isHidden: false
    sortIndex: -1
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
  country:
    input: select
    accessorKey: country
    key: country
    id: country
    label: country
    position: 100
    skipPersist: false
    isHidden: false
    sortIndex: -1
    options:
      - { label: "United States", backgroundColor: "hsl(200, 95%, 90%)"}
      - { label: "Hungary", backgroundColor: "hsl(140, 95%, 90%)"}
      - { label: "Spain", backgroundColor: "hsl(288, 95%, 90%)"}
      - { label: "Czech Republic", backgroundColor: "hsl(304, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
  ethnicity:
    input: select
    accessorKey: ethnicity
    key: ethnicity
    id: ethnicity
    label: ethnicity
    position: 100
    skipPersist: false
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Caucasian", backgroundColor: "hsl(260, 95%, 90%)"}
      - { label: "Latin", backgroundColor: "hsl(149, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
  status:
    input: select
    accessorKey: status
    key: status
    id: status
    label: status
    position: 100
    skipPersist: false
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Active", backgroundColor: "hsl(292, 95%, 90%)"}
      - { label: "Retired", backgroundColor: "hsl(42, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
config:
  remove_field_when_delete_column: false
  cell_size: "normal"
  sticky_first_column: false
  group_folder_column: ""
  remove_empty_folders: false
  automatically_group_files: false
  hoist_files_with_empty_attributes: true
  show_metadata_created: false
  show_metadata_modified: false
  show_metadata_tasks: false
  show_metadata_inlinks: false
  show_metadata_outlinks: false
  source_data: "current_folder"
  source_form_result: "root"
  source_destination_path: "/"
  row_templates_folder: "/"
  current_row_template: ""
  pagination_size: 10
  font_size: 16
  enable_js_formulas: false
  formula_folder_path: "/"
  inline_default: false
  inline_new_position: "last_field"
  date_format: "yyyy-MM-dd"
  datetime_format: "yyyy-MM-dd HH:mm:ss"
  metadata_date_format: "yyyy-MM-dd HH:mm:ss"
  enable_footer: false
filters:
  enabled: false
  conditions:
```