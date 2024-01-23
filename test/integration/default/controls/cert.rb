# frozen_string_literal: true

control "Cert x509 #{os.name}" do
  title 'Test x509 cert files'

  crts = {
    'standalone.gn98.de' => {
      'alias' => 'www.standalone.gn98.de',
      'keylength' => 2048,
    },
    'alpn.gn98.de' => {
      'keylength' => 4096,
    }
  }
  crts.each do |cn, conf|
    dir = "/home/vagrant/crt/#{cn}"

    describe x509_certificate("#{dir}/fullchain.cer") do
      it { should be_certificate }
      its('subject.CN') { should eq cn }
      its('keylength') { should eq conf['keylength'] }
      its('subject_alt_names') { should include "DNS:#{conf['alias']}" } if conf['alias']
      its('validity_in_days') { should be > 30 }
    end
  end
end
