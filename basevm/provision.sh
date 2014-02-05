sudo apt-get update
sudo apt-get install -y ansible
sudo ansible-playbook -i /vagrant/ansible/hosts /vagrant/ansible/site.yml
sudo ansible-playbook -i /vagrant/sym-playbook/hosts /vagrant/ansible/site.yml