# tryit
## Modules

### results_analyzer

`analyze_test_results(result_file_path)` loads a new test results JSON, compares the labs against the latest `patient_profile` resource using GPT-4.1, and stores a summary in `test_results_summary` resources via `resource_api`.

