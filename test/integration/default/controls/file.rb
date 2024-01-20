# frozen_string_literal: true

control "Cert files #{os.name}" do
  title 'Test cert files'

  dir = '/home/vagrant/crt/acmeshtest.gn98.de'

  describe directory(dir) do
    it { should exist }
  end

  describe file("#{dir}/fullchain.cer") do
    it { should exist }
  end

  describe file("#{dir}/acmeshtest.gn98.de.key") do
    it { should exist }
  end
end
