module Gitlab
  module LDAP
    class Access
      attr_reader :adapter

      def self.open(&block)
        Gitlab::LDAP::Adapter.open do |adapter|
          block.call(self.new(adapter))
        end
      end

      def self.allowed?(user)
        self.open do |access|
          if access.allowed?(user)
            # GitLab EE LDAP code goes here
            user.last_credential_check_at = Time.now
            user.save
            true
          else
            false
          end
        end
      end

      def initialize(adapter=nil)
        @adapter = adapter
      end

      def allowed?(user)
				# not using Active Directory where users can be disabled
        true;
      end
    end
  end
end
