class { 'elasticsearch':
  package_url => 'https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.0.0/elasticsearch-2.0.0.deb',
  java_install => true,
  config => {
    'node' => {
      'name' => 'siroopelastic01'
    }
  }
}