variable "raspberry_pi_ip" {
  description = "The IP address of the Raspberry Pi"
  type        = string
}

variable "ssh_user" {
  description = "SSH username for Raspberry Pi access"
  type        = string
}

variable "ssh_password" {
  description = "SSH password for Raspberry Pi access"
  type        = string
  sensitive   = true  # Mark as sensitive to avoid showing in logs
}

