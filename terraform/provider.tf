terraform {
  required_providers {
    proxmox = {
      source = "bpg/proxmox"
    }
  }

  backend "s3" {
    bucket = "terraform-state"
    key    = "micro-paas/terraform.tfstate"
    region = "us-east-1"

    endpoints = {
      s3 = "http://10.100.110.100:9000"
    }

    use_path_style              = true
    skip_credentials_validation = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
    skip_metadata_api_check     = true
  }
}

provider "proxmox" {
  insecure = true
}