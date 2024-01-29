# frozen_string_literal: true

control "Cert files #{os.name} #{os.release}" do
  title 'Test cert files'

  crts = ['standalone.gn98.de', 'alpn.gn98.de']

  crts.each do |crt|
    dir = "/home/vagrant/crt/#{crt}"

    describe directory(dir) do
      it { should exist }
    end

    describe file("#{dir}/fullchain.cer") do
      it { should exist }
    end

    describe file("#{dir}/#{crt}.key") do
      it { should exist }
    end
  end
end
