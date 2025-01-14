locals {
  function_apps = {
    python : {
      runtime                              = "python",
      version                              = "~4",
      mi_blobServiceName                   = "",
      mi_blobServiceUri                    = null,
      mi_queueServiceName                  = "",
      mi_queueServiceUri                   = null,
      mi_accountName                       = "",
      mi_accountValue                      = null,
      SCM_DO_BUILD_DURING_DEPLOYMENT       = 1,
      ENABLE_ORYX_BUILD                    = true,
      fhir_url                             = null,
      AzureWebJobs_convertToFhir_Disabled  = 0,
      always_on                            = true,
      WEBSITE_RUN_FROM_PACKAGE             = null,
      AzureWebJobs_IntakePipeline_Disabled = 0,
      AzureWebJobsStorage__accountName     = "${var.resource_prefix}datasa",
      AzureWebJobsStorage__blobServiceUri  = "https://${var.resource_prefix}datasa.blob.core.windows.net",
      AzureWebJobsStorage__queueServiceUri = "https://${var.resource_prefix}datasa.queue.core.windows.net",
      AzureWebJobsStorage__tableServiceUri = "https://${var.resource_prefix}datasa.table.core.windows.net",
      INVALID_OUTPUT_CONTAINER_PATH        = "blob-trigger-out/invalid-messages",
      VALID_OUTPUT_CONTAINER_PATH          = "blob-trigger-out/valid-messages",
      CSV_INPUT_PREFIX                     = "blob-trigger-out/valid-messages/",
      CSV_OUTPUT_PREFIX                    = "csvs"
    }
  }
}
