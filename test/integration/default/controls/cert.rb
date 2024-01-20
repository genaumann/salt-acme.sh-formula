# frozen_string_literal: true

control "Cert x509 #{os.name}" do
  title 'Test x509 cert files'

  dir = '/home/vagrant/crt/acmeshtest.gn98.de'

  describe x509_certificate("#{dir}/fullchain.cer") do
    it { should be_certificate }
    its('key_length') { should be 4096 }
    its('subject.CN') { should eq 'acmeshtest.gn98.de' }
    its('validity_in_days') { should be > 30 }
  end
end
