provider "null" {}

resource "null_resource" "install_k3s" {
  connection {
    type     = "ssh"
    host     = var.raspberry_pi_ip
    user     = var.ssh_user
    password = var.ssh_password
  }

  provisioner "remote-exec" {
    inline = [
      # Check if k3s service is active, proceed with installation if not
      "if ! systemctl is-active --quiet k3s; then curl -sfL https://get.k3s.io | sh -; fi"
    ]
  }
}
