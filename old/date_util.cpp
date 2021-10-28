#include "date_util.hpp"

namespace fraud_detection
{
	namespace Date_Util
	{
		unsigned
		get_year_from_string(std::string date){
			std::istringstream is(date);
			unsigned d, m, y;
			char delimiter;
			if (is >> d >> delimiter >> m >> delimiter >> y) {
				return y;
			}
			return 0;
		}
	}
}